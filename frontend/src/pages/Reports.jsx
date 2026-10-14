import React, { useState } from 'react'
import { reports } from '../services/api'
import { FileText, Download, BarChart3, PieChart as PieChartIcon } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts'

const COLORS = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#ec4899', '#8b5cf6', '#14b8a6']

export default function Reports() {
  const [activeTab, setActiveTab] = useState('monthly')
  const [month, setMonth] = useState(new Date().getMonth() + 1)
  const [year, setYear] = useState(new Date().getFullYear())
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(false)
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const fetchMonthly = async () => {
    setLoading(true)
    try {
      const data = await reports.getMonthly(month, year)
      setReport(data)
    } catch (err) {
      setReport({ error: err.message })
    } finally {
      setLoading(false)
    }
  }

  const fetchYearly = async () => {
    setLoading(true)
    try {
      const data = await reports.getYearly(year)
      setReport(data)
    } catch (err) {
      setReport({ error: err.message })
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    if (!startDate || !endDate) return alert('Please select a date range')
    reports.download(startDate, endDate)
  }

  const fmt = (n) => `$${(n || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}`

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Reports</h2>
          <p>Generate and download financial reports</p>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        <button className={`btn ${activeTab === 'monthly' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => { setActiveTab('monthly'); setReport(null) }}>
          <BarChart3 size={16} /> Monthly
        </button>
        <button className={`btn ${activeTab === 'yearly' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => { setActiveTab('yearly'); setReport(null) }}>
          <PieChartIcon size={16} /> Yearly
        </button>
        <button className={`btn ${activeTab === 'download' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setActiveTab('download')}>
          <Download size={16} /> Download
        </button>
      </div>

      {activeTab === 'monthly' && (
        <div className="card">
          <div style={{ display: 'flex', gap: 12, marginBottom: 20, alignItems: 'flex-end', flexWrap: 'wrap' }}>
            <div className="form-group" style={{ marginBottom: 0, minWidth: 120 }}>
              <label>Month</label>
              <select value={month} onChange={e => setMonth(Number(e.target.value))}>
                {Array.from({ length: 12 }, (_, i) => (
                  <option key={i + 1} value={i + 1}>{new Date(2024, i).toLocaleString('en', { month: 'long' })}</option>
                ))}
              </select>
            </div>
            <div className="form-group" style={{ marginBottom: 0, minWidth: 100 }}>
              <label>Year</label>
              <select value={year} onChange={e => setYear(Number(e.target.value))}>
                {Array.from({ length: 5 }, (_, i) => <option key={i} value={new Date().getFullYear() - 2 + i}>{new Date().getFullYear() - 2 + i}</option>)}
              </select>
            </div>
            <button className="btn btn-primary" onClick={fetchMonthly} disabled={loading}>{loading ? 'Loading...' : 'Generate Report'}</button>
          </div>
          {report && !report.error && (
            <div>
              <div className="stat-cards">
                <div className="stat-card income">
                  <div className="label">Income</div>
                  <div className="value" style={{ color: 'var(--success)', fontSize: 22 }}>{fmt(report.total_income || report.totalIncome)}</div>
                </div>
                <div className="stat-card expense">
                  <div className="label">Expenses</div>
                  <div className="value" style={{ color: 'var(--danger)', fontSize: 22 }}>{fmt(report.total_expenses || report.totalExpenses)}</div>
                </div>
                <div className="stat-card balance">
                  <div className="label">Net</div>
                  <div className="value" style={{ color: 'var(--primary)', fontSize: 22 }}>{fmt((report.total_income || 0) - (report.total_expenses || 0))}</div>
                </div>
              </div>
              {report.category_breakdown && report.category_breakdown.length > 0 && (
                <div style={{ marginTop: 20 }}>
                  <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Spending Breakdown</h3>
                  <ResponsiveContainer width="100%" height={280}>
                    <BarChart data={report.category_breakdown}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis dataKey="category" stroke="#64748b" fontSize={12} />
                      <YAxis stroke="#64748b" fontSize={12} />
                      <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#f1f5f9' }} />
                      <Bar dataKey="amount" fill="#6366f1" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              )}
              {report.transactions && (
                <div style={{ marginTop: 20 }}>
                  <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Transactions ({report.transactions.length})</h3>
                  <div className="table-container">
                    <table>
                      <thead>
                        <tr><th>Date</th><th>Description</th><th>Category</th><th>Amount</th></tr>
                      </thead>
                      <tbody>
                        {report.transactions.map((tx, i) => (
                          <tr key={i}>
                            <td>{new Date(tx.date).toLocaleDateString()}</td>
                            <td>{tx.description}</td>
                            <td><span className="tag tag-info">{tx.category}</span></td>
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
          )}
          {report?.error && <p style={{ color: 'var(--danger)' }}>{report.error}</p>}
        </div>
      )}

      {activeTab === 'yearly' && (
        <div className="card">
          <div style={{ display: 'flex', gap: 12, marginBottom: 20, alignItems: 'flex-end' }}>
            <div className="form-group" style={{ marginBottom: 0, minWidth: 100 }}>
              <label>Year</label>
              <select value={year} onChange={e => setYear(Number(e.target.value))}>
                {Array.from({ length: 5 }, (_, i) => <option key={i} value={new Date().getFullYear() - 2 + i}>{new Date().getFullYear() - 2 + i}</option>)}
              </select>
            </div>
            <button className="btn btn-primary" onClick={fetchYearly} disabled={loading}>{loading ? 'Loading...' : 'Generate Report'}</button>
          </div>
          {report && !report.error && (
            <div>
              <div className="stat-cards">
                <div className="stat-card income">
                  <div className="label">Total Income</div>
                  <div className="value" style={{ color: 'var(--success)', fontSize: 22 }}>{fmt(report.total_income || report.totalIncome)}</div>
                </div>
                <div className="stat-card expense">
                  <div className="label">Total Expenses</div>
                  <div className="value" style={{ color: 'var(--danger)', fontSize: 22 }}>{fmt(report.total_expenses || report.totalExpenses)}</div>
                </div>
                <div className="stat-card balance">
                  <div className="label">Net Savings</div>
                  <div className="value" style={{ color: 'var(--primary)', fontSize: 22 }}>{fmt((report.total_income || 0) - (report.total_expenses || 0))}</div>
                </div>
              </div>
              {report.monthly_summary && (
                <div style={{ marginTop: 20 }}>
                  <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Monthly Breakdown</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={report.monthly_summary}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis dataKey="month" stroke="#64748b" fontSize={12} />
                      <YAxis stroke="#64748b" fontSize={12} />
                      <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#f1f5f9' }} />
                      <Legend />
                      <Bar dataKey="income" fill="#10b981" name="Income" radius={[4, 4, 0, 0]} />
                      <Bar dataKey="expenses" fill="#ef4444" name="Expenses" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              )}
            </div>
          )}
          {report?.error && <p style={{ color: 'var(--danger)' }}>{report.error}</p>}
        </div>
      )}

      {activeTab === 'download' && (
        <div className="card">
          <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Download Report</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: 20, fontSize: 14 }}>Select a date range to download a CSV report of your transactions.</p>
          <div className="form-row" style={{ maxWidth: 400 }}>
            <div className="form-group">
              <label>Start Date</label>
              <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
            </div>
            <div className="form-group">
              <label>End Date</label>
              <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />
            </div>
          </div>
          <button className="btn btn-primary" onClick={handleDownload} style={{ marginTop: 8 }}>
            <Download size={16} /> Download CSV
          </button>
        </div>
      )}
    </div>
  )
}
