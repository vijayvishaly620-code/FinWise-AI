import React, { useState, useContext } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { AuthContext } from '../App'
import { LayoutDashboard, ArrowLeftRight, PiggyBank, Target, Bot, FileText, User, LogOut, Menu, X, Database } from 'lucide-react'

export default function Layout({ children }) {
  const { user, logout } = useContext(AuthContext)
  const location = useLocation()
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/transactions', label: 'Transactions', icon: ArrowLeftRight },
    { path: '/budgets', label: 'Budgets', icon: PiggyBank },
    { path: '/savings', label: 'Savings Goals', icon: Target },
    { path: '/advisor', label: 'AI Advisor', icon: Bot },
    { path: '/reports', label: 'Reports', icon: FileText },
    { path: '/dataset', label: 'Dataset', icon: Database },
  ]

  const handleLogout = () => { logout(); navigate('/') }

  return (
    <div className="app-layout">
      <button className="btn btn-ghost" onClick={() => setSidebarOpen(!sidebarOpen)}
        style={{ position: 'fixed', top: 16, left: 16, zIndex: 200, display: 'none' }}
        id="menu-btn">
        {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
      </button>
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-logo">
          <div>
            <h1>FinWise AI</h1>
            <span>Personal Finance Advisor</span>
          </div>
        </div>
        <nav className="sidebar-nav">
          {navItems.map(item => (
            <Link key={item.path} to={item.path} className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
              onClick={() => setSidebarOpen(false)}>
              <item.icon size={18} />
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="sidebar-footer">
          <Link to="/profile" className={`nav-item ${location.pathname === '/profile' ? 'active' : ''}`}>
            <User size={18} />
            Profile
          </Link>
          <button className="nav-item" onClick={handleLogout} style={{ width: '100%', border: 'none', background: 'none', cursor: 'pointer', fontFamily: 'inherit' }}>
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </aside>
      <main className="main-content">
        {children}
      </main>
    </div>
  )
}
