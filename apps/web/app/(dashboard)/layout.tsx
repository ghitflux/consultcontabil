'use client';

import { useState } from 'react';
import { Button, Link, Avatar, Dropdown, DropdownTrigger, DropdownMenu, DropdownItem } from '@/heroui';
import { NotificationCenter } from '@/components/shared/NotificationCenter';
import { ThemeSwitcher } from '@/components/shared/ThemeSwitcher';
import {
  HomeIcon,
  UsersIcon,
  FileTextIcon as DocumentIcon,
  DollarSignIcon as CurrencyIcon,
  LicenseIcon as ShieldIcon,
  BarChartIcon as ChartIcon,
  ClockIcon,
  MenuIcon,
} from '@/lib/icons';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Clientes', href: '/clientes', icon: UsersIcon },
    { name: 'Obrigações', href: '/obrigacoes', icon: DocumentIcon },
    { name: 'Financeiro', href: '/financeiro', icon: CurrencyIcon },
    { name: 'Licenças', href: '/licencas', icon: ShieldIcon },
    { name: 'Relatórios', href: '/relatorios', icon: ChartIcon },
    { name: 'Atividades', href: '/atividades', icon: ClockIcon },
  ];

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside
        className={`${
          sidebarOpen ? 'w-64' : 'w-0'
        } flex flex-col border-r border-divider transition-all duration-300 md:w-64`}
      >
        <div className="flex h-16 items-center justify-between border-b border-divider px-6">
          <h2 className="text-xl font-bold">SaaS Contábil</h2>
        </div>
        <nav className="flex-1 space-y-1 px-3 py-4">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                href={item.href}
                className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-default-600 transition-colors hover:bg-default-100 hover:text-default-900"
              >
                <Icon className="h-5 w-5" />
                {item.name}
              </Link>
            );
          })}
        </nav>
        <div className="border-t border-divider p-4">
          <p className="text-xs text-default-400">Marco 1 - Em Desenvolvimento</p>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex flex-1 flex-col">
        {/* Header */}
        <header className="flex h-16 items-center justify-between border-b border-divider px-6">
          <Button
            isIconOnly
            variant="light"
            onPress={() => setSidebarOpen(!sidebarOpen)}
            className="md:hidden"
          >
            <MenuIcon className="h-6 w-6" />
          </Button>

          <div className="flex-1" />

          <div className="flex items-center gap-4">
            {/* Theme Switcher */}
            <ThemeSwitcher />

            {/* Notification Center */}
            <NotificationCenter />

            {/* User Menu */}
            <Dropdown placement="bottom-end">
              <DropdownTrigger>
                <Avatar
                  as="button"
                  className="cursor-pointer"
                  name="Admin"
                  size="sm"
                />
              </DropdownTrigger>
              <DropdownMenu aria-label="Profile Actions">
                <DropdownItem key="profile" className="gap-2">
                  <p className="font-semibold">Usuário Mock</p>
                  <p className="text-sm">admin@example.com</p>
                </DropdownItem>
                <DropdownItem key="settings">Configurações</DropdownItem>
                <DropdownItem key="logout" color="danger">
                  Sair
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-6">{children}</main>
      </div>
    </div>
  );
}
