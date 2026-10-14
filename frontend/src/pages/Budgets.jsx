import React, { useState, useEffect } from 'react'
import { budgets } from '../services/api'
import { Plus, Edit2, Trash2, X, PiggyBank } from 'lucide-react'

const CATEGORIES = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Bills', 'Health', 'Education', 'Other']

export default function Budgets() {
  const [budgetList, setBudgetList] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editItem, setEditItem] = useState(null)
  const [currentMonth, setCurrentMonth] = useState(() => new Date().toISOString().slice(0, 7))
  const [form, setForm] = useState({ category: 'Food', limit_amount: '', month: new Date().toISOString().slice(0, 7) })
  const [saving, setSaving] = useState(false)

  const fetchBudgets = async () => {
    setLoading(true)
    try {
      const data = await budgets.getAll(currentMonth)
      setBudgetList(data.budgets || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchBudgets() }, [currentMonth])

  const openAdd = () => { setEditItem(null); setForm({ category: 'Food', limit_amount: '', month: currentMonth }); setShowModal(true) }
  const openEdit = (b) => { setEditItem(b); setForm({ category: b.category, limit_amount: String(b.limit_amount), month: b.month }); setShowModal(true) }

  const handleSave = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      const payload = { ...form, limit_amount: parseFloat(form.limit_amount) }
      if (editItem) {
        await budgets.update(editItem.id || editItem._id, payload)
      } else {
        await budgets.create(payload)
      }
      setShowModal(false)
      fetchBudgets()
    } catch (err) {
      alert(err.message)
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this budget?')) return
    try {
      await budgets.delete(id)
      fetchBudgets()
    } catch (err) {
      alert(err.message)
    }
  }

  const fmt = (n) => `$${Number(n).toLocaleString('en-US', { minimumFractionDigits: 2 })}`

  const getStatus = (spent, limit) => {
    const pct = (spent / limit) * 100
    if (pct >= 100) return { class: 'exceeded', label: 'Exceeded', color: 'var(--danger)' }
    if (pct >= 80) return { class: 'warning', label: 'Warning', color: 'var(--warning)' }
    return { class: 'ok', label: 'On Track', color: 'var(--success)' }
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Budgets</h2>
          <p>Set and track monthly spending limits</p>
        </div>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <input type="month" value={currentMonth} onChange={e => setCurrentMonth(e.target.value)}
            style={{ padding: '8px 12px', background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 8, color: 'var(--text)', fontSize: 14 }} />
          <button className="btn btn-primary" onClick={openAdd}><Plus size={16} /> Add Budget</button>
        </div>
      </div>

      {loading ? <div style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>Loading...</div> : budgetList.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: 60 }}>
          <PiggyBank size={48} style={{ color: 'var(--text-muted)', marginBottom: 16 }} />
          <h3 style={{ marginBottom: 8 }}>No Budgets Set</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: 20 }}>Create your first budget to start tracking spending</p>
          <button className="btn btn-primary" onClick={openAdd}>Create Budget</button>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 16 }}>
          {budgetList.map(b => {
            const spent = b.spent || b.total_spent || 0
            const pct = Math.min((spent / b.limit_amount) * 100, 100)
            const status = getStatus(spent, b.limit_amount)
            return (
              <div key={b.id || b._id} className="card" style={{ borderLeft: `3px solid ${status.color}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                  <div>
                    <h3 style={{ fontSize: 16, fontWeight: 600 }}>{b.category}</h3>
                    <span className="tag tag-info" style={{ marginTop: 4 }}>{status.label}</span>
                  </div>
                  <div style={{ display: 'flex', gap: 4 }}>
                    <button className="btn btn-ghost btn-sm" onClick={() => openEdit(b)}><Edit2 size={14} /></button>
                    <button className="btn btn-ghost btn-sm" onClick={() => handleDelete(b.id || b._id)} style={{ color: 'var(--danger)' }}><Trash2 size={14} /></button>
                  </div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>Spent: {fmt(spent)}</span>
                  <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>Limit: {fmt(b.limit_amount)}</span>
                </div>
                <div className="progress-bar">
                  <div className={`fill ${status.class}`} style={{ width: `${pct}%` }} />
                </div>
                <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 6, textAlign: 'right' }}>
                  {pct.toFixed(0)}% used
                  {spent > b.limit_amount && ` — ${fmt(spent - b.limit_amount)} over budget`}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
              <h3>{editItem ? 'Edit Budget' : 'Add Budget'}</h3>
              <button className="btn btn-ghost btn-sm" onClick={() => setShowModal(false)}><X size={18} /></button>
            </div>
            <form onSubmit={handleSave}>
              <div className="form-row">
                <div className="form-group">
                  <label>Category</label>
                  <select value={form.category} onChange={e => setForm({...form, category: e.target.value})} disabled={!!editItem}>
                    {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
                <div className="form-group">
                  <label>Monthly Limit</label>
                  <input type="number" step="0.01" min="1" value={form.limit_amount} onChange={e => setForm({...form, limit_amount: e.target.value})} required placeholder="0.00" />
                </div>
              </div>
              <div className="form-group">
                <label>Month</label>
                <input type="month" value={form.month} onChange={e => setForm({...form, month: e.target.value})} />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary" disabled={saving}>{saving ? 'Saving...' : (editItem ? 'Update' : 'Create')}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
