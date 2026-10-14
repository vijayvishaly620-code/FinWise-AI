import React, { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts'
import { Database, Table, BarChart3, PieChart as PieIcon, Activity } from 'lucide-react'
import { dataset } from '../services/api'

const COLORS = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#64748b']

export default function Dataset() {
  const [info, setInfo] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    dataset.getInfo()
      .then(setInfo)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="page-header"><h2>Loading dataset...</h2></div>
  if (error) return <div className="page-header"><h2>Error: {error}</h2></div>
  if (!info) return <div className="page-header"><h2>Dataset not found</h2></div>

  const healthData = Object.entries(info.health_distribution || {}).map(([name, value]) => ({ name, value }))
  const empData = Object.entries(info.employment_distribution || {}).map(([name, value]) => ({ name, value }))
  const goalData = Object.entries(info.goal_distribution || {}).map(([name, value]) => ({ name, value }))

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Dataset Insights</h2>
          <p>{info.name} - {info.records.toLocaleString()} synthetic financial records for ML training</p>
        </div>
      </div>

      <div className="stat-cards">
        <div className="stat-card income">
          <div className="label"><Database size={16} /> Records</div>
          <div className="value">{info.records.toLocaleString()}</div>
        </div>
        <div className="stat-card balance">
          <div className="label"><Table size={16} /> Features</div>
          <div className="value">{info.columns}</div>
        </div>
        <div className="stat-card expense">
          <div className="label"><Activity size={16} /> Missing Values</div>
          <div className="value">{info.missing_values}</div>
        </div>
        <div className="stat-card savings">
          <div className="label">Avg Income</div>
          <div className="value">{info.numeric_stats?.income_mean?.toLocaleString()}</div>
        </div>
        <div className="stat-card health">
          <div className="label">Avg Savings Rate</div>
          <div className="value">{info.numeric_stats?.savings_rate_mean}%</div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3><BarChart3 size={18} style={{ marginRight: 8, verticalAlign: 'middle' }} />Financial Health Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={healthData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <YAxis tick={{ fill: '#94a3b8' }} />
              <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#f1f5f9' }} />
              <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                {healthData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3><PieIcon size={18} style={{ marginRight: 8, verticalAlign: 'middle' }} />Employment Type Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={empData} cx="50%" cy="50%" outerRadius={100} dataKey="value" label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                {empData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#f1f5f9' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3><BarChart3 size={18} style={{ marginRight: 8, verticalAlign: 'middle' }} />Financial Goal Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={goalData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} angle={-30} textAnchor="end" height={80} />
              <YAxis tick={{ fill: '#94a3b8' }} />
              <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#f1f5f9' }} />
              <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                {goalData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Dataset Features</h3>
          <div style={{ maxHeight: 300, overflowY: 'auto' }}>
            <table>
              <thead><tr><th>#</th><th>Column Name</th><th>Type</th></tr></thead>
              <tbody>
                {info.column_names?.map((col, i) => (
                  <tr key={i}>
                    <td>{i + 1}</td>
                    <td style={{ fontFamily: 'monospace', fontSize: 13 }}>{col}</td>
                    <td><span className={`tag ${['monthly_income','monthly_expenses','food_expense','transport_expense','shopping_expense','bill_expense','education_expense','entertainment_expense','healthcare_expense','rent_expense','travel_expense','other_expense','monthly_savings','existing_debt','budget_amount','budget_used_percentage','savings_rate','expense_ratio','goal_progress','credit_score','age'].includes(col) ? 'tag-income' : 'tag-info'}`}>
                      {['monthly_income','monthly_expenses','food_expense','transport_expense','shopping_expense','bill_expense','education_expense','entertainment_expense','healthcare_expense','rent_expense','travel_expense','other_expense','monthly_savings','existing_debt','budget_amount','budget_used_percentage','savings_rate','expense_ratio','goal_progress','credit_score','age'].includes(col) ? 'Numeric' : 'Categorical'}
                    </span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: 16 }}>
        <h3 style={{ marginBottom: 16 }}>Data Preview (First 10 Records)</h3>
        <div className="table-container" style={{ maxHeight: 400, overflowY: 'auto' }}>
          <table>
            <thead>
              <tr>
                <th>ID</th><th>Age</th><th>Employment</th><th>Income</th><th>Expenses</th><th>Savings</th><th>Savings Rate</th><th>Debt</th><th>Credit</th><th>Health</th>
              </tr>
            </thead>
            <tbody>
              {info.preview?.map((row, i) => (
                <tr key={i}>
                  <td style={{ fontFamily: 'monospace' }}>{row.user_id}</td>
                  <td>{row.age}</td>
                  <td>{row.employment_type}</td>
                  <td>{row.monthly_income?.toLocaleString()}</td>
                  <td>{row.monthly_expenses?.toLocaleString()}</td>
                  <td>{row.monthly_savings?.toLocaleString()}</td>
                  <td><span className={`tag ${row.savings_rate >= 20 ? 'tag-ok' : row.savings_rate >= 10 ? 'tag-info' : 'tag-warning'}`}>{row.savings_rate}%</span></td>
                  <td>{row.existing_debt?.toLocaleString()}</td>
                  <td>{row.credit_score}</td>
                  <td><span className={`tag ${row.financial_health === 'Excellent' ? 'tag-ok' : row.financial_health === 'Good' ? 'tag-info' : row.financial_health === 'Needs Improvement' ? 'tag-warning' : 'tag-critical'}`}>{row.financial_health}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
