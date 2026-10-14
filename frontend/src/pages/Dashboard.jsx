import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { dashboard, transactions } from '../services/api'
import { TrendingUp, TrendingDown, Wallet, PiggyBank, ArrowLeftRight, Plus } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar, Legend } from 'recharts'

const COLORS = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#ec4899', '#8b5cf6', '#14b8a6']

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [analytics, setAnalytics] = useState(null)
  const [recentTx, setRecentTx] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      dashboard.getSummary().catch(() => null),
      dashboard.getAnalytics().catch(() => null),
      transactions.getAll('limit=5').catch(() => ({ transactions: [] }))
    ]).then(([s, a, t]) => {
      setSummary(s)
      setAnalytics(a)
      setRecentTx(t.transactions || [])
    }).finally(() => setLoading(false))
  }, [])

  const fmt = (n) => `$${(n || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`

  if (loading) return <div style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>Loading dashboard...</div>

  const totalIncome = summary?.total_income || summary?.totalIncome || 0
  const totalExpenses = summary?.total_expenses || summary?.totalExpenses || 0
  const balance = totalIncome - totalExpenses
  const savingsAmount = summary?.total_savings || summary?.totalSavings || 0

  const monthlyData = analytics?.monthly_trends || analytics?.monthlyTrends || []
  const categoryData = analytics?.category_breakdown || analytics?.categoryBreakdown || []

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Dashboard</h2>
          <p>Your financial overview at a glance</p>
        </div>
        <Link to="/transactions" className="btn btn-primary"><Plus size={16} /> Add Transaction</Link>
      </div>

      <div className="stat-cards">
        <div className="stat-card income">
          <div className="label"><TrendingUp size={16} /> Total Income</div>
          <div className="value" style={{ color: 'var(--success)' }}>{fmt(totalIncome)}</div>
        </div>
        <div className="stat-card expense">
          <div className="label"><TrendingDown size={16} /> Total Expenses</div>
          <div className="value" style={{ color: 'var(--danger)' }}>{fmt(totalExpenses)}</div>
        </div>
        <div className="stat-card balance">
          <div className="label"><Wallet size={16} /> Balance</div>
          <div className="value" style={{ color: balance >= 0 ? 'var(--primary)' : 'var(--danger)' }}>{fmt(balance)}</div>
        </div>
        <div className="stat-card savings">
          <div className="label"><PiggyBank size={16} /> Savings</div>
          <div className="value" style={{ color: 'var(--secondary)' }}>{fmt(savingsAmount)}</div>
        </div>
      </div>

      <div className="charts-grid">
        {monthlyData.length > 0 && (
          <div className="chart-card">
            <h3>Monthly Trends</h3>
            <ResponsiveContainer width="100%" height={280}>
              <AreaChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="month" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#f1f5f9' }} />
                <Area type="monotone" dataKey="income" stroke="#10b981" fill="#10b98120" name="Income" />
                <Area type="monotone" dataKey="expenses" stroke="#ef4444" fill="#ef444420" name="Expenses" />
                <Legend />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        )}

        {categoryData.length > 0 && (
          <div className="chart-card">
            <h3>Spending by Category</h3>
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={categoryData} dataKey="amount" nameKey="category" cx="50%" cy="50%" outerRadius={100} label={({ category, percent }) => `${category} ${(percent * 100).toFixed(0)}%`}>
                  {categoryData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#f1f5f9' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {recentTx.length > 0 && (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <h3 style={{ fontSize: 16, fontWeight: 600 }}>Recent Transactions</h3>
            <Link to="/transactions" className="btn btn-ghost btn-sm">View All</Link>
          </div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Description</th>
                  <th>Category</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                {recentTx.map(tx => (
                  <tr key={tx.id || tx._id}>
                    <td>{new Date(tx.date).toLocaleDateString()}</td>
                    <td>{tx.description}</td>
                    <td><span className={`tag tag-${tx.type === 'income' ? 'income' : 'expense'}`}>{tx.category}</span></td>
                    <td style={{ fontWeight: 600, color: tx.type === 'income' ? 'var(--success)' : 'var(--danger)' }}>
                      {tx.type === 'income' ? '+' : '-'}{fmt(tx.amount)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
