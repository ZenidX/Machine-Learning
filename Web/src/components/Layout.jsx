import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Home, CalendarRange, Code2, Brain, Gamepad2, Wrench } from 'lucide-react'

const navigation = [
  { name: 'Inici', href: '/', icon: Home },
  { name: 'Programa', href: '/programa', icon: CalendarRange },
  { name: 'Python i dades', href: '/python', icon: Code2 },
  { name: 'Machine Learning', href: '/machine-learning', icon: Brain },
  { name: 'Xarxes i RL', href: '/deep-rl', icon: Gamepad2 },
  { name: 'Recursos', href: '/recursos', icon: Wrench },
]

export default function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()

  const isActive = (href) => {
    if (href === '/') return location.pathname === '/'
    return location.pathname.startsWith(href)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside className={`
        fixed top-0 left-0 z-50 h-full w-72 bg-white shadow-xl transform transition-transform duration-300 flex flex-col
        lg:translate-x-0
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex items-center justify-between h-16 px-6 border-b flex-shrink-0">
          <Link to="/" className="flex items-center space-x-2" onClick={() => setSidebarOpen(false)}>
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">ML</span>
            </div>
            <div className="leading-tight">
              <span className="font-bold text-gray-900 block">Machine Learning</span>
              <span className="text-xs text-gray-500">Curs 2026-27</span>
            </div>
          </Link>
          <button
            className="lg:hidden p-2 rounded-md hover:bg-gray-100"
            onClick={() => setSidebarOpen(false)}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <nav className="p-4 space-y-1 overflow-y-auto flex-1">
          {navigation.map((item) => (
            <Link
              key={item.href}
              to={item.href}
              onClick={() => setSidebarOpen(false)}
              className={`
                flex items-center space-x-3 px-4 py-3 rounded-lg
                ${isActive(item.href)
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-gray-700 hover:bg-gray-100'}
              `}
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.name}</span>
            </Link>
          ))}
        </nav>

        <div className="p-4 border-t bg-gray-50 flex-shrink-0">
          <div className="text-xs text-gray-500">
            <p className="font-medium text-gray-700">Optativa · CFGS</p>
            <p>DAM i DAW · 2n curs</p>
          </div>
        </div>
      </aside>

      <div className="lg:pl-72">
        <header className="sticky top-0 z-30 h-16 bg-white border-b flex items-center px-4 lg:px-8">
          <button
            className="lg:hidden p-2 rounded-md hover:bg-gray-100"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="w-6 h-6" />
          </button>
          <div className="ml-4 lg:ml-0 min-w-0">
            <h1 className="text-base lg:text-lg font-semibold text-gray-900 truncate">
              Aprenentatge automàtic · Machine Learning
            </h1>
          </div>
        </header>

        <main className="p-4 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  )
}
