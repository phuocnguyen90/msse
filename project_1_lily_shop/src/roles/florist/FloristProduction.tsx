import { useState } from 'react';
import { ArrowLeft, Clock, AlertCircle, Check, Package, MoreHorizontal } from 'lucide-react';
import { productionOrders } from '../../data/mockData';

interface FloristProductionProps {
  onBack: () => void;
}

type OrderStatus = 'to-make' | 'in-progress' | 'completed';

interface Order {
  id: string;
  customer: string;
  bouquet: string;
  ingredients: { name: string; quantity: number }[];
  status: OrderStatus;
  priority: 'high' | 'normal';
  deliveryTime: string;
  note: string;
}

function FloristProduction({ onBack }: FloristProductionProps) {
  const [orders, setOrders] = useState<Order[]>(productionOrders as Order[]);
  const [draggedOrder, setDraggedOrder] = useState<string | null>(null);

  const columns: { id: OrderStatus; title: string; color: string }[] = [
    { id: 'to-make', title: 'To Make', color: 'bg-amber-100 text-amber-700' },
    { id: 'in-progress', title: 'In Progress', color: 'bg-sky-100 text-sky-700' },
    { id: 'completed', title: 'Completed', color: 'bg-emerald-100 text-emerald-700' }
  ];

  const handleDragStart = (orderId: string) => {
    setDraggedOrder(orderId);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent, newStatus: OrderStatus) => {
    e.preventDefault();
    if (draggedOrder) {
      setOrders(prev => 
        prev.map(order => 
          order.id === draggedOrder 
            ? { ...order, status: newStatus }
            : order
        )
      );
      setDraggedOrder(null);
    }
  };

  const getOrdersByStatus = (status: OrderStatus) => {
    return orders.filter(order => order.status === status);
  };

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
                <span className="text-2xl">✂️</span>
                <span className="font-heading font-semibold text-xl text-[#2A2A2A]">
                  Production Board
                </span>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="hidden md:flex items-center gap-2 px-4 py-2 bg-[#E8F2E8] rounded-full">
                <Clock className="w-4 h-4 text-[#8BA078]" />
                <span className="text-sm font-medium text-[#2A2A2A]">
                  {new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              <div className="flex items-center gap-2 px-4 py-2 bg-amber-100 rounded-full">
                <Package className="w-4 h-4 text-amber-700" />
                <span className="text-sm font-medium text-amber-700">
                  {orders.filter(o => o.status !== 'completed').length} pending
                </span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content - Kanban Board */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid md:grid-cols-3 gap-6">
          {columns.map((column) => {
            const columnOrders = getOrdersByStatus(column.id);
            
            return (
              <div
                key={column.id}
                className="flex flex-col"
                onDragOver={handleDragOver}
                onDrop={(e) => handleDrop(e, column.id)}
              >
                {/* Column Header */}
                <div className={`flex items-center justify-between p-4 rounded-t-2xl ${column.color}`}>
                  <div className="flex items-center gap-2">
                    <h3 className="font-heading font-semibold">{column.title}</h3>
                    <span className="px-2 py-0.5 bg-white/50 rounded-full text-xs font-medium">
                      {columnOrders.length}
                    </span>
                  </div>
                  <MoreHorizontal className="w-5 h-5 opacity-50" />
                </div>

                {/* Column Content */}
                <div className="flex-1 bg-white/50 rounded-b-2xl p-4 min-h-[500px]">
                  <div className="space-y-4">
                    {columnOrders.map((order) => (
                      <OrderCard
                        key={order.id}
                        order={order}
                        onDragStart={() => handleDragStart(order.id)}
                      />
                    ))}
                    {columnOrders.length === 0 && (
                      <div className="text-center py-12 text-[#6E6E6E]">
                        <p className="text-sm">No orders</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );
}

// Order Card Component
interface OrderCardProps {
  order: Order;
  onDragStart: () => void;
}

function OrderCard({ order, onDragStart }: OrderCardProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div
      draggable
      onDragStart={onDragStart}
      className={`bg-white rounded-xl p-4 shadow-sm cursor-move hover:shadow-md transition-all ${
        order.priority === 'high' ? 'border-l-4 border-amber-500' : ''
      }`}
    >
      {/* Card Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-mono text-[#6E6E6E]">{order.id}</span>
            {order.priority === 'high' && (
              <span className="px-2 py-0.5 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">
                Priority
              </span>
            )}
          </div>
          <h4 className="font-heading font-semibold text-lg text-[#2A2A2A]">
            {order.bouquet}
          </h4>
        </div>
        <div className="flex items-center gap-1 text-sm text-[#6E6E6E]">
          <Clock className="w-4 h-4" />
          <span>{order.deliveryTime}</span>
        </div>
      </div>

      {/* Customer Name (no financial info) */}
      <p className="text-sm text-[#6E6E6E] mb-3">
        For: <span className="font-medium text-[#2A2A2A]">{order.customer}</span>
      </p>

      {/* Recipe Ingredients - LARGE FONT for easy reading */}
      <div className="bg-[#F6F7F3] rounded-lg p-4 mb-3">
        <p className="text-xs font-medium text-[#6E6E6E] uppercase tracking-wide mb-2">
          Recipe
        </p>
        <ul className="space-y-2">
          {order.ingredients.map((ingredient, index) => (
            <li 
              key={index}
              className="flex items-center justify-between"
            >
              <span className="text-lg text-[#2A2A2A]">{ingredient.name}</span>
              <span className="text-2xl font-bold text-[#E57F84]">
                ×{ingredient.quantity}
              </span>
            </li>
          ))}
        </ul>
      </div>

      {/* Special Instructions */}
      {order.note && (
        <div className="flex items-start gap-2 p-3 bg-amber-50 rounded-lg mb-3">
          <AlertCircle className="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0" />
          <p className="text-sm text-amber-800">{order.note}</p>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center justify-between pt-2 border-t border-[rgba(139,160,120,0.15)]">
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-sm text-[#6E6E6E] hover:text-[#2A2A2A] transition-colors"
        >
          {expanded ? 'Show less' : 'More details'}
        </button>
        {order.status === 'in-progress' && (
          <button className="flex items-center gap-1 px-3 py-1.5 bg-emerald-100 text-emerald-700 rounded-full text-sm font-medium">
            <Check className="w-4 h-4" />
            Mark Done
          </button>
        )}
      </div>
    </div>
  );
}

export default FloristProduction;
