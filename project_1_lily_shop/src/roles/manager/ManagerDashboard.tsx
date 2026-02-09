import { useState } from 'react';
import { ArrowLeft, TrendingUp, Package, AlertTriangle, DollarSign, ShoppingCart, RefreshCw } from 'lucide-react';
import { dashboardMetrics, inventory, recipes } from '../../data/mockData';

interface ManagerDashboardProps {
  onBack: () => void;
}

// Component annotations for design choices and traceability:
//
// 1. Navigation setup (FR-22) - Manager requires overview + inventory views
//    Design choice: Sticky navigation with clear view switching for operational efficiency
//    Traces to FR-22 (Manager Dashboard) and US-11 (Centralized Order Dashboard)
//
// 2. Color scheme (NFR-01) - Soft greens and pinks to match floral branding
//    Design choice: #E57F84 (rose) for primary actions, #F6F7F3 (cream) background
//    Traces to NFR-01 (Responsiveness) and brand consistency requirements
//
// 3. Real-time data (FR-22) - Low stock items highlighted in red
//    Design choice: Visual warning system with color coding for critical alerts
//    Traces to FR-22 (Low Stock Alerts) and FR-13 (Low Stock threshold logic)
//
// 4. Quick restock functionality (FR-14) - Allow manual inventory adjustment
//    Design choice: +50 increment buttons for rapid restocking during busy periods
//    Traces to FR-14 (Manual Adjustments) and operational efficiency needs

type ManagerView = 'overview' | 'inventory';

function ManagerDashboard({ onBack }: ManagerDashboardProps) {
  const [currentView, setCurrentView] = useState<ManagerView>('overview');
  const [inventoryData, setInventoryData] = useState(inventory);

  const handleRestock = (itemId: number) => {
    setInventoryData(prev => 
      prev.map(item => 
        item.id === itemId 
          ? { ...item, quantity: item.quantity + 50, status: 'good' as const }
          : item
      )
    );
  };

  const lowStockItems = inventoryData.filter(item => item.status === 'low');

  return (
    <div className="min-h-screen bg-[#F6F7F3]">
      <div className="grain-overlay" />
      
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-[rgba(139,160,120,0.15)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-4">
              <button
                onClick={onBack}
                className="p-2 hover:bg-[#E8F2E8] rounded-full transition-colors"
              >
                <ArrowLeft className="w-5 h-5 text-[#6E6E6E]" />
              </button>
              <div className="flex items-center gap-2">
                <span className="text-2xl">📊</span>
                <span className="font-heading font-semibold text-xl text-[#2A2A2A]">
                  Manager Dashboard
                </span>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <button
                onClick={() => setCurrentView('overview')}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  currentView === 'overview' 
                    ? 'bg-[#E57F84] text-white' 
                    : 'text-[#6E6E6E] hover:bg-[#E8F2E8]'
                }`}
              >
                Overview
              </button>
              <button
                onClick={() => setCurrentView('inventory')}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  currentView === 'inventory' 
                    ? 'bg-[#E57F84] text-white' 
                    : 'text-[#6E6E6E] hover:bg-[#E8F2E8]'
                }`}
              >
                Inventory
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentView === 'overview' ? (
          <OverviewView 
            metrics={dashboardMetrics}
            lowStockItems={lowStockItems}
            onRestock={handleRestock}
          />
        ) : (
          <InventoryView 
            inventory={inventoryData}
            recipes={recipes}
            onRestock={handleRestock}
          />
        )}
      </main>
    </div>
  );
}

// Overview View Component
interface OverviewViewProps {
  metrics: typeof dashboardMetrics;
  lowStockItems: typeof inventory;
  onRestock: (itemId: number) => void;
}

function OverviewView({ metrics, lowStockItems, onRestock }: OverviewViewProps) {
  const statCards = [
    {
      title: 'Total Sales',
      value: `$${metrics.totalSales.toLocaleString()}`,
      change: '+12%',
      icon: TrendingUp,
      color: 'bg-emerald-100 text-emerald-600'
    },
    {
      title: 'Orders Today',
      value: metrics.ordersToday.toString(),
      change: '+5',
      icon: ShoppingCart,
      color: 'bg-[#E57F84]/10 text-[#E57F84]'
    },
    {
      title: 'Revenue Today',
      value: `$${metrics.revenueToday.toLocaleString()}`,
      change: '+8%',
      icon: DollarSign,
      color: 'bg-amber-100 text-amber-600'
    },
    {
      title: 'Pending Orders',
      value: metrics.pendingOrders.toString(),
      change: '2 urgent',
      icon: Package,
      color: 'bg-sky-100 text-sky-600'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Stats Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <div
            key={index}
            className="bg-white rounded-[24px] p-6 shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`w-12 h-12 ${stat.color} rounded-xl flex items-center justify-center`}>
                <stat.icon className="w-6 h-6" />
              </div>
              <span className={`text-sm font-medium ${
                stat.change.includes('+') ? 'text-emerald-600' : 'text-amber-600'
              }`}>
                {stat.change}
              </span>
            </div>
            <h3 className="text-3xl font-heading font-bold text-[#2A2A2A]">
              {stat.value}
            </h3>
            <p className="text-[#6E6E6E] text-sm mt-1">{stat.title}</p>
          </div>
        ))}
      </div>

      {/* Low Stock Alert Widget */}
      <div className="bg-white rounded-[24px] p-6 shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-amber-100 rounded-xl flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-amber-600" />
            </div>
            <div>
              <h2 className="text-xl font-heading font-semibold text-[#2A2A2A]">
                Low Stock Alert
              </h2>
              <p className="text-sm text-[#6E6E6E]">
                {lowStockItems.length} items need attention
              </p>
            </div>
          </div>
          <button 
            onClick={() => {}}
            className="text-sm text-[#E57F84] font-medium hover:underline"
          >
            View All
          </button>
        </div>

        {lowStockItems.length > 0 ? (
          <div className="space-y-3">
            {lowStockItems.map((item) => (
              <div
                key={item.id}
                className="flex items-center justify-between p-4 bg-amber-50 rounded-xl border border-amber-100"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
                    <Package className="w-5 h-5 text-amber-600" />
                  </div>
                  <div>
                    <h4 className="font-medium text-[#2A2A2A]">{item.name}</h4>
                    <p className="text-sm text-amber-700">
                      Only {item.quantity} {item.unit} left
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => onRestock(item.id)}
                  className="flex items-center gap-2 px-4 py-2 bg-amber-600 text-white rounded-full text-sm font-medium hover:bg-amber-700 transition-colors"
                >
                  <RefreshCw className="w-4 h-4" />
                  Restock
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-[#6E6E6E]">
            <p>All items are well stocked! 🎉</p>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-[#E8F2E8] rounded-[24px] p-6">
          <h3 className="text-lg font-heading font-semibold text-[#2A2A2A] mb-4">
            Quick Actions
          </h3>
          <div className="space-y-3">
            <button className="w-full p-4 bg-white rounded-xl text-left hover:shadow-md transition-shadow">
              <span className="font-medium text-[#2A2A2A]">View Today's Orders</span>
              <p className="text-sm text-[#6E6E6E]">Check pending and in-progress orders</p>
            </button>
            <button className="w-full p-4 bg-white rounded-xl text-left hover:shadow-md transition-shadow">
              <span className="font-medium text-[#2A2A2A]">Generate Sales Report</span>
              <p className="text-sm text-[#6E6E6E]">Download weekly or monthly report</p>
            </button>
            <button className="w-full p-4 bg-white rounded-xl text-left hover:shadow-md transition-shadow">
              <span className="font-medium text-[#2A2A2A]">Manage Staff Schedule</span>
              <p className="text-sm text-[#6E6E6E]">Update florist and driver shifts</p>
            </button>
          </div>
        </div>

        <div className="bg-white rounded-[24px] p-6 shadow-sm">
          <h3 className="text-lg font-heading font-semibold text-[#2A2A2A] mb-4">
            Weekly Overview
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-[#6E6E6E]">Revenue Target</span>
                <span className="font-medium">$12,450 / $15,000</span>
              </div>
              <div className="h-3 bg-[#F6F7F3] rounded-full overflow-hidden">
                <div 
                  className="h-full bg-[#E57F84] rounded-full"
                  style={{ width: '83%' }}
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-[#6E6E6E]">Order Fulfillment</span>
                <span className="font-medium">98%</span>
              </div>
              <div className="h-3 bg-[#F6F7F3] rounded-full overflow-hidden">
                <div 
                  className="h-full bg-emerald-500 rounded-full"
                  style={{ width: '98%' }}
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-[#6E6E6E]">Customer Satisfaction</span>
                <span className="font-medium">4.8/5.0</span>
              </div>
              <div className="h-3 bg-[#F6F7F3] rounded-full overflow-hidden">
                <div 
                  className="h-full bg-amber-500 rounded-full"
                  style={{ width: '96%' }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Inventory View Component
interface InventoryViewProps {
  inventory: typeof inventory;
  recipes: typeof recipes;
  onRestock: (itemId: number) => void;
}

function InventoryView({ inventory, recipes, onRestock }: InventoryViewProps) {
  return (
    <div className="space-y-8">
      {/* Raw Materials Table */}
      <div className="bg-white rounded-[24px] p-6 shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-heading font-semibold text-[#2A2A2A]">
            Raw Materials Inventory
          </h2>
          <button className="px-4 py-2 bg-[#E8F2E8] text-[#2A2A2A] rounded-full text-sm font-medium hover:bg-[#8BA078]/20 transition-colors">
            Export CSV
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-[rgba(139,160,120,0.15)]">
                <th className="text-left py-3 px-4 text-sm font-medium text-[#6E6E6E]">Item</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-[#6E6E6E]">Quantity</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-[#6E6E6E]">Status</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-[#6E6E6E]">Min Level</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-[#6E6E6E]">Action</th>
              </tr>
            </thead>
            <tbody>
              {inventory.map((item) => (
                <tr 
                  key={item.id} 
                  className="border-b border-[rgba(139,160,120,0.1)] hover:bg-[#F6F7F3] transition-colors"
                >
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-[#E8F2E8] rounded-lg flex items-center justify-center">
                        <Package className="w-4 h-4 text-[#8BA078]" />
                      </div>
                      <span className="font-medium text-[#2A2A2A]">{item.name}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`font-semibold ${
                      item.status === 'low' ? 'text-amber-600' : 'text-[#2A2A2A]'
                    }`}>
                      {item.quantity}
                    </span>
                    <span className="text-sm text-[#6E6E6E] ml-1">{item.unit}</span>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium ${
                      item.status === 'low' 
                        ? 'bg-amber-100 text-amber-700' 
                        : 'bg-emerald-100 text-emerald-700'
                    }`}>
                      {item.status === 'low' ? (
                        <AlertTriangle className="w-3 h-3" />
                      ) : (
                        <TrendingUp className="w-3 h-3" />
                      )}
                      {item.status === 'low' ? 'Low Stock' : 'Good'}
                    </span>
                  </td>
                  <td className="py-4 px-4 text-sm text-[#6E6E6E]">
                    {item.minLevel} {item.unit}
                  </td>
                  <td className="py-4 px-4">
                    <button
                      onClick={() => onRestock(item.id)}
                      className="flex items-center gap-2 px-4 py-2 bg-[#E8F2E8] text-[#2A2A2A] rounded-full text-sm font-medium hover:bg-[#8BA078]/30 transition-colors"
                    >
                      <RefreshCw className="w-4 h-4" />
                      Restock
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Product Recipes */}
      <div className="bg-white rounded-[24px] p-6 shadow-sm">
        <h2 className="text-xl font-heading font-semibold text-[#2A2A2A] mb-6">
          Product Recipes
        </h2>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recipes.map((recipe) => (
            <div
              key={recipe.id}
              className="p-5 bg-[#F6F7F3] rounded-xl border border-[rgba(139,160,120,0.15)]"
            >
              <h3 className="font-heading font-semibold text-lg text-[#2A2A2A] mb-4">
                {recipe.name}
              </h3>
              <ul className="space-y-2">
                {recipe.ingredients.map((ingredient, index) => (
                  <li 
                    key={index}
                    className="flex items-center justify-between text-sm"
                  >
                    <span className="text-[#6E6E6E]">{ingredient.name}</span>
                    <span className="font-medium text-[#2A2A2A]">
                      {ingredient.quantity} {ingredient.name.includes('stems') ? 'stems' : 'units'}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ManagerDashboard;
