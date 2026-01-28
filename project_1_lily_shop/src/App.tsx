import { useState } from 'react';
import { Flower2, UserCog, Scissors, Truck } from 'lucide-react';
import CustomerExperience from './roles/customer/CustomerExperience';
import ManagerDashboard from './roles/manager/ManagerDashboard';
import FloristProduction from './roles/florist/FloristProduction';
import DriverLogistics from './roles/driver/DriverLogistics';

type UserRole = 'selector' | 'customer' | 'manager' | 'florist' | 'driver';

function App() {
  const [currentRole, setCurrentRole] = useState<UserRole>('selector');

  const roles = [
    {
      id: 'customer' as UserRole,
      title: 'Customer',
      subtitle: 'Shop & Order',
      description: 'Browse bouquets, place orders, and track deliveries',
      icon: Flower2,
      color: 'bg-rose-100 text-rose-600',
      borderColor: 'border-rose-200'
    },
    {
      id: 'manager' as UserRole,
      title: 'Manager',
      subtitle: 'Admin Dashboard',
      description: 'View metrics, manage inventory, and monitor operations',
      icon: UserCog,
      color: 'bg-emerald-100 text-emerald-600',
      borderColor: 'border-emerald-200'
    },
    {
      id: 'florist' as UserRole,
      title: 'Florist',
      subtitle: 'Production',
      description: 'View orders, follow recipes, and prepare bouquets',
      icon: Scissors,
      color: 'bg-amber-100 text-amber-600',
      borderColor: 'border-amber-200'
    },
    {
      id: 'driver' as UserRole,
      title: 'Driver',
      subtitle: 'Logistics',
      description: 'View delivery routes and confirm drop-offs',
      icon: Truck,
      color: 'bg-sky-100 text-sky-600',
      borderColor: 'border-sky-200'
    }
  ];

  if (currentRole === 'customer') {
    return <CustomerExperience onBack={() => setCurrentRole('selector')} />;
  }

  if (currentRole === 'manager') {
    return <ManagerDashboard onBack={() => setCurrentRole('selector')} />;
  }

  if (currentRole === 'florist') {
    return <FloristProduction onBack={() => setCurrentRole('selector')} />;
  }

  if (currentRole === 'driver') {
    return <DriverLogistics onBack={() => setCurrentRole('selector')} />;
  }

  return (
    <div className="min-h-screen bg-[#F6F7F3] flex items-center justify-center p-4">
      <div className="grain-overlay" />
      
      <div className="w-full max-w-5xl">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Flower2 className="w-10 h-10 text-[#E57F84]" />
            <h1 className="text-4xl md:text-5xl font-heading font-bold text-[#2A2A2A]">
              Lily's Florist
            </h1>
          </div>
          <p className="text-[#6E6E6E] text-lg font-body">
            Select your role to continue
          </p>
        </div>

        {/* Role Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {roles.map((role) => {
            const Icon = role.icon;
            return (
              <button
                key={role.id}
                onClick={() => setCurrentRole(role.id)}
                className={`group relative bg-white rounded-[28px] p-8 border-2 ${role.borderColor} 
                  shadow-sm hover:shadow-xl transition-all duration-300 text-left
                  hover:-translate-y-1`}
              >
                <div className="flex items-start gap-5">
                  <div className={`${role.color} p-4 rounded-2xl`}>
                    <Icon className="w-8 h-8" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h2 className="text-2xl font-heading font-semibold text-[#2A2A2A]">
                        {role.title}
                      </h2>
                      <span className="text-sm font-label uppercase tracking-wider text-[#6E6E6E]">
                        {role.subtitle}
                      </span>
                    </div>
                    <p className="text-[#6E6E6E] font-body">
                      {role.description}
                    </p>
                  </div>
                </div>
                
                <div className="absolute bottom-6 right-6 opacity-0 group-hover:opacity-100 transition-opacity">
                  <span className="text-[#E57F84] font-medium text-sm">
                    Enter →
                  </span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-[#6E6E6E] text-sm font-body">
          <p>Fresh flowers, delivered with care</p>
        </div>
      </div>
    </div>
  );
}

export default App;
