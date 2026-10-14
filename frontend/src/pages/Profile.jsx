import React, { useState, useEffect, useContext } from 'react'
import { AuthContext } from '../App'
import { auth } from '../services/api'
import { User, Mail, Save, Bell, Shield } from 'lucide-react'

export default function Profile() {
  const { user, login } = useContext(AuthContext)
  const [form, setForm] = useState({ name: '', email: '', monthly_income: '', currency: 'USD' })
  const [password, setPassword] = useState({ current: '', newPass: '', confirm: '' })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('profile')

  useEffect(() => {
    if (user) {
      setForm({
        name: user.name || '',
        email: user.email || '',
        monthly_income: String(user.monthly_income || ''),
        currency: user.currency || 'USD'
      })
    }
  }, [user])

  const handleProfileSave = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setMessage('')
    try {
      const payload = { ...form }
      if (payload.monthly_income) payload.monthly_income = parseFloat(payload.monthly_income)
      const data = await auth.updateProfile(payload)
      if (data.user) login(localStorage.getItem('token'), data.user)
      setMessage('Profile updated successfully!')
    } catch (err) {
      setError(err.message || 'Update failed')
    } finally {
      setLoading(false)
    }
  }

  if (!user) return <div style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>Loading profile...</div>

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Profile</h2>
          <p>Manage your account settings</p>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        <button className={`btn ${activeTab === 'profile' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setActiveTab('profile')}>
          <User size={16} /> Profile
        </button>
        <button className={`btn ${activeTab === 'notifications' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setActiveTab('notifications')}>
          <Bell size={16} /> Notifications
        </button>
        <button className={`btn ${activeTab === 'security' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setActiveTab('security')}>
          <Shield size={16} /> Security
        </button>
      </div>

      {activeTab === 'profile' && (
        <div className="card" style={{ maxWidth: 600 }}>
          <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 20 }}>Personal Information</h3>
          {message && <div style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)', color: 'var(--success)', padding: '10px 14px', borderRadius: 8, marginBottom: 16, fontSize: 13 }}>{message}</div>}
          {error && <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', color: 'var(--danger)', padding: '10px 14px', borderRadius: 8, marginBottom: 16, fontSize: 13 }}>{error}</div>}
          <form onSubmit={handleProfileSave}>
            <div className="form-group">
              <label><User size={14} style={{ display: 'inline', marginRight: 4 }} /> Full Name</label>
              <input type="text" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required />
            </div>
            <div className="form-group">
              <label><Mail size={14} style={{ display: 'inline', marginRight: 4 }} /> Email</label>
              <input type="email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} required />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Monthly Income (estimated)</label>
                <input type="number" step="0.01" min="0" value={form.monthly_income} onChange={e => setForm({...form, monthly_income: e.target.value})} placeholder="0.00" />
              </div>
              <div className="form-group">
                <label>Currency</label>
                <select value={form.currency} onChange={e => setForm({...form, currency: e.target.value})}>
                  <option value="USD">USD ($)</option>
                  <option value="EUR">EUR (&euro;)</option>
                  <option value="GBP">GBP (&pound;)</option>
                  <option value="INR">INR (&#8377;)</option>
                </select>
              </div>
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading} style={{ marginTop: 8 }}>
              <Save size={16} /> {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </form>
        </div>
      )}

      {activeTab === 'notifications' && (
        <div className="card" style={{ maxWidth: 600 }}>
          <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 20 }}>Notification Preferences</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {[
              { label: 'Budget alerts', desc: 'Get notified when spending approaches or exceeds budget limits' },
              { label: 'Goal milestones', desc: 'Celebrate when you reach savings goal milestones' },
              { label: 'Unusual spending', desc: 'Alerts for transactions that are significantly higher than usual' },
              { label: 'Monthly summary', desc: 'Receive a monthly financial health summary' },
            ].map((item, i) => (
              <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderBottom: '1px solid var(--border)' }}>
                <div>
                  <div style={{ fontWeight: 500, fontSize: 14 }}>{item.label}</div>
                  <div style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{item.desc}</div>
                </div>
                <label style={{ position: 'relative', display: 'inline-block', width: 44, height: 24 }}>
                  <input type="checkbox" defaultChecked={i < 2} style={{ opacity: 0, width: 0, height: 0 }} />
                  <span style={{ position: 'absolute', cursor: 'pointer', inset: 0, background: 'var(--bg)', borderRadius: 12, transition: '0.3s', border: '1px solid var(--border)' }}>
                    <span style={{ position: 'absolute', content: '', height: 18, width: 18, left: i < 2 ? 22 : 2, bottom: 2, background: i < 2 ? 'var(--primary)' : 'var(--text-muted)', borderRadius: '50%', transition: '0.3s' }} />
                  </span>
                </label>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'security' && (
        <div className="card" style={{ maxWidth: 600 }}>
          <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 20 }}>Change Password</h3>
          <form onSubmit={(e) => { e.preventDefault(); alert('Password change requires backend implementation') }}>
            <div className="form-group">
              <label>Current Password</label>
              <input type="password" value={password.current} onChange={e => setPassword({...password, current: e.target.value})} required />
            </div>
            <div className="form-group">
              <label>New Password</label>
              <input type="password" value={password.newPass} onChange={e => setPassword({...password, newPass: e.target.value})} required minLength={6} />
            </div>
            <div className="form-group">
              <label>Confirm New Password</label>
              <input type="password" value={password.confirm} onChange={e => setPassword({...password, confirm: e.target.value})} required />
            </div>
            <button type="submit" className="btn btn-primary" style={{ marginTop: 8 }}>
              <Shield size={16} /> Update Password
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
