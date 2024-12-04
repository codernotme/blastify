import Link from 'next/link'
import { Home, Mail, Settings, HelpCircle, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { ThemeToggle } from '@/components/theme-toggle'

interface SidebarProps {
  open: boolean
  setOpen: (open: boolean) => void
}

const Sidebar: React.FC<SidebarProps> = ({ open, setOpen }) => {
  return (
    <div className={`
      fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out
      ${open ? 'translate-x-0' : '-translate-x-full'}
      md:relative md:translate-x-0
    `}>
      <div className="flex items-center justify-between p-4">
        <Link href="/" className="flex items-center space-x-2">
          <Mail className="h-8 w-8 text-blue-600" />
          <span className="text-2xl font-bold text-gray-800 dark:text-white">Blastify</span>
        </Link>
        <Button
          variant="ghost"
          className="md:hidden"
          onClick={() => setOpen(false)}
        >
          <X className="h-6 w-6" />
        </Button>
      </div>
      <ScrollArea className="flex-1 px-3">
        <nav className="space-y-1 py-4">
          <NavItem href="/" icon={Home}>Dashboard</NavItem>
          <NavItem href="/campaigns" icon={Mail}>Campaigns</NavItem>
          <NavItem href="/settings" icon={Settings}>Settings</NavItem>
          <NavItem href="/help" icon={HelpCircle}>Help</NavItem>
        </nav>
      </ScrollArea>
      <div className="p-4">
        <ThemeToggle />
      </div>
    </div>
  )
}

interface NavItemProps {
  href: string
  icon: React.ElementType
  children: React.ReactNode
}

const NavItem: React.FC<NavItemProps> = ({ href, icon: Icon, children }) => (
  <Link
    href={href}
    className="flex items-center space-x-3 px-3 py-2 rounded-md text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition duration-150 ease-in-out"
  >
    <Icon className="h-5 w-5" />
    <span>{children}</span>
  </Link>
)

export default Sidebar

