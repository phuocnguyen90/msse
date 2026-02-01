import { useState, useRef } from 'react';
import { ArrowLeft, MapPin, Phone, MessageSquare, Navigation, Check, Package, Clock, ChevronRight } from 'lucide-react';
import { deliveryOrders } from '../../data/mockData';

interface DriverLogisticsProps {
  onBack: () => void;
}

// Component annotations for design choices and traceability:
//
// 1. Privacy protection (FR-24) - Hide financial data from driver view
//    Design choice: Only show Name, Address, Phone, Instructions - no pricing or totals
//    Traces to FR-24 (Driver privacy) and US-15 (Security by role)
//
// 2. Mobile optimization (NFR-01) - Large touch targets for in-vehicle use
//    Design choice: 44px minimum touch targets, clear icons for quick recognition
//    Traces to NFR-01 (Mobile responsiveness) and driver workflow efficiency
//
// 3. Real-time status tracking (FR-25) - One-tap delivery confirmation
//    Design choice: Simple "Delivered" button with immediate status update
//    Traces to FR-25 (Status workflow) and US-11 (Order management)
//
// 4. Zone-based routing (FR-16) - Geographic organization of deliveries
//    Design choice: Group orders by zone for optimized delivery routes
//    Traces to FR-16 (Zone pricing) and operational efficiency

interface DeliveryOrder {
  id: string;
  recipient: string;
  address: string;
  phone: string;
  instructions: string;
  zone: string;
  status: 'ready' | 'delivered';
  bouquet: string;
}

function DriverLogistics({ onBack }: DriverLogisticsProps) {
  const [orders, setOrders] = useState<DeliveryOrder[]>(deliveryOrders as DeliveryOrder[]);
  const [selectedOrder, setSelectedOrder] = useState<DeliveryOrder | null>(null);

  const handleDeliver = (orderId: string) => {
    setOrders((prev: DeliveryOrder[]) => 
      prev.map((order: DeliveryOrder) => 
        order.id === orderId 
          ? { ...order, status: 'delivered' as const }
          : order
      )
    );
    setSelectedOrder(null);
  };

  const pendingOrders = orders.filter(o => o.status === 'ready');
  const completedOrders = orders.filter(o => o.status === 'delivered');

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
                <span className="text-2xl">🚚</span>
                <span className="font-heading font-semibold text-xl text-[#2A2A2A]">
                  Delivery Manifest
                </span>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-4 py-2 bg-[#E8F2E8] rounded-full">
                <Package className="w-4 h-4 text-[#8BA078]" />
                <span className="text-sm font-medium text-[#2A2A2A]">
                  {pendingOrders.length} remaining
                </span>
              </div>
              <div className="flex items-center gap-2 px-4 py-2 bg-emerald-100 rounded-full">
                <Check className="w-4 h-4 text-emerald-700" />
                <span className="text-sm font-medium text-emerald-700">
                  {completedOrders.length} done
                </span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Delivery List */}
          <div>
            <h2 className="text-xl font-heading font-semibold text-[#2A2A2A] mb-4">
              Ready for Delivery
            </h2>
            <div className="space-y-4">
              {pendingOrders.map((order, index) => (
                <DeliveryCard
                  key={order.id}
                  order={order}
                  index={index + 1}
                  isSelected={selectedOrder?.id === order.id}
                  onClick={() => setSelectedOrder(order)}
                />
              ))}
              {pendingOrders.length === 0 && (
                <div className="text-center py-12 bg-white rounded-[24px]">
                  <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Check className="w-8 h-8 text-emerald-600" />
                  </div>
                  <h3 className="text-lg font-heading font-semibold text-[#2A2A2A] mb-2">
                    All deliveries completed!
                  </h3>
                  <p className="text-[#6E6E6E]">Great job today!</p>
                </div>
              )}
            </div>

            {/* Completed Deliveries */}
            {completedOrders.length > 0 && (
              <div className="mt-8">
                <h2 className="text-xl font-heading font-semibold text-[#2A2A2A] mb-4">
                  Completed
                </h2>
                <div className="space-y-2">
                  {completedOrders.map((order) => (
                    <div
                      key={order.id}
                      className="p-4 bg-emerald-50 rounded-xl opacity-60"
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium text-[#2A2A2A]">{order.recipient}</p>
                          <p className="text-sm text-[#6E6E6E]">{order.address}</p>
                        </div>
                        <Check className="w-5 h-5 text-emerald-600" />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Selected Order Detail / Map Area */}
          <div className="lg:sticky lg:top-24 lg:h-fit">
            {selectedOrder ? (
              <OrderDetailPanel
                order={selectedOrder}
                onDeliver={() => handleDeliver(selectedOrder.id)}
              />
            ) : (
              <div className="bg-white rounded-[24px] p-8 text-center">
                <div className="w-20 h-20 bg-[#E8F2E8] rounded-full flex items-center justify-center mx-auto mb-4">
                  <Navigation className="w-10 h-10 text-[#8BA078]" />
                </div>
                <h3 className="text-xl font-heading font-semibold text-[#2A2A2A] mb-2">
                  Select a delivery
                </h3>
                <p className="text-[#6E6E6E]">
                  Tap on an order to view details and confirm delivery
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

// Delivery Card Component
interface DeliveryCardProps {
  order: DeliveryOrder;
  index: number;
  isSelected: boolean;
  onClick: () => void;
}

function DeliveryCard({ order, index, isSelected, onClick }: DeliveryCardProps) {
  return (
    <div
      onClick={onClick}
      className={`p-5 rounded-xl cursor-pointer transition-all ${
        isSelected 
          ? 'bg-[#E57F84] text-white shadow-lg' 
          : 'bg-white hover:shadow-md'
      }`}
    >
      <div className="flex items-start gap-4">
        <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
          isSelected ? 'bg-white/20' : 'bg-[#E8F2E8]'
        }`}>
          <span className={`font-heading font-bold ${isSelected ? 'text-white' : 'text-[#8BA078]'}`}>
            {index}
          </span>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <h4 className={`font-heading font-semibold truncate ${
              isSelected ? 'text-white' : 'text-[#2A2A2A]'
            }`}>
              {order.recipient}
            </h4>
            <span className={`px-2 py-0.5 rounded-full text-xs ${
              isSelected ? 'bg-white/20 text-white' : 'bg-[#E8F2E8] text-[#8BA078]'
            }`}>
              {order.zone}
            </span>
          </div>
          <p className={`text-sm truncate ${isSelected ? 'text-white/80' : 'text-[#6E6E6E]'}`}>
            {order.address}
          </p>
          {order.instructions && (
            <p className={`text-sm mt-2 truncate ${isSelected ? 'text-white/70' : 'text-amber-600'}`}>
              📝 {order.instructions}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

// Order Detail Panel with Slide to Confirm
interface OrderDetailPanelProps {
  order: DeliveryOrder;
  onDeliver: () => void;
}

function OrderDetailPanel({ order, onDeliver }: OrderDetailPanelProps) {
  const [isDelivering, setIsDelivering] = useState(false);
  const sliderRef = useRef<HTMLDivElement>(null);
  const [sliderPosition, setSliderPosition] = useState(0);
  const [isDragging, setIsDragging] = useState(false);

  const handleMouseDown = () => {
    setIsDragging(true);
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging || !sliderRef.current) return;
    
    const rect = sliderRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const maxX = rect.width - 64;
    const newPosition = Math.max(0, Math.min(x, maxX));
    setSliderPosition(newPosition);

    if (newPosition >= maxX * 0.9) {
      setIsDelivering(true);
      setTimeout(() => {
        onDeliver();
        setIsDelivering(false);
        setSliderPosition(0);
      }, 300);
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    if (sliderPosition < (sliderRef.current?.offsetWidth || 0) - 64 - 20) {
      setSliderPosition(0);
    }
  };

  const handleTouchStart = () => {
    setIsDragging(true);
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isDragging || !sliderRef.current) return;
    
    const rect = sliderRef.current.getBoundingClientRect();
    const x = e.touches[0].clientX - rect.left;
    const maxX = rect.width - 64;
    const newPosition = Math.max(0, Math.min(x, maxX));
    setSliderPosition(newPosition);

    if (newPosition >= maxX * 0.9) {
      setIsDelivering(true);
      setTimeout(() => {
        onDeliver();
        setIsDelivering(false);
        setSliderPosition(0);
      }, 300);
    }
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
    if (sliderPosition < (sliderRef.current?.offsetWidth || 0) - 64 - 20) {
      setSliderPosition(0);
    }
  };

  return (
    <div className="bg-white rounded-[24px] p-6 shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <p className="text-sm text-[#6E6E6E] mb-1">Order {order.id}</p>
          <h3 className="text-2xl font-heading font-bold text-[#2A2A2A]">
            {order.recipient}
          </h3>
        </div>
        <div className="w-12 h-12 bg-[#E8F2E8] rounded-full flex items-center justify-center">
          <Package className="w-6 h-6 text-[#8BA078]" />
        </div>
      </div>

      {/* Delivery Details - NO PRICES */}
      <div className="space-y-4 mb-6">
        <div className="flex items-start gap-3 p-4 bg-[#F6F7F3] rounded-xl">
          <MapPin className="w-5 h-5 text-[#8BA078] mt-0.5 flex-shrink-0" />
          <div>
            <p className="font-medium text-[#2A2A2A]">Delivery Address</p>
            <p className="text-[#6E6E6E]">{order.address}</p>
            <p className="text-sm text-[#8BA078] mt-1">{order.zone}</p>
          </div>
        </div>

        <div className="flex items-start gap-3 p-4 bg-[#F6F7F3] rounded-xl">
          <Phone className="w-5 h-5 text-[#8BA078] mt-0.5 flex-shrink-0" />
          <div>
            <p className="font-medium text-[#2A2A2A]">Contact</p>
            <a 
              href={`tel:${order.phone}`}
              className="text-[#E57F84] font-medium"
            >
              {order.phone}
            </a>
          </div>
        </div>

        {order.instructions && (
          <div className="flex items-start gap-3 p-4 bg-amber-50 rounded-xl border border-amber-100">
            <MessageSquare className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
            <div>
              <p className="font-medium text-amber-800">Special Instructions</p>
              <p className="text-amber-700">{order.instructions}</p>
            </div>
          </div>
        )}

        <div className="flex items-start gap-3 p-4 bg-[#F6F7F3] rounded-xl">
          <Clock className="w-5 h-5 text-[#8BA078] mt-0.5 flex-shrink-0" />
          <div>
            <p className="font-medium text-[#2A2A2A]">Bouquet</p>
            <p className="text-[#6E6E6E]">{order.bouquet}</p>
          </div>
        </div>
      </div>

      {/* Map Button */}
      <button className="w-full p-4 bg-[#E8F2E8] rounded-xl flex items-center justify-center gap-2 text-[#2A2A2A] font-medium hover:bg-[#8BA078]/20 transition-colors mb-6">
        <Navigation className="w-5 h-5" />
        Open in Maps
      </button>

      {/* Slide to Confirm */}
      <div 
        ref={sliderRef}
        className="relative h-16 bg-emerald-100 rounded-full overflow-hidden cursor-pointer select-none"
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {/* Background Text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`font-medium transition-opacity ${
            sliderPosition > 20 ? 'opacity-0' : 'opacity-100 text-emerald-700'
          }`}>
            {isDelivering ? 'Delivered!' : 'Slide to confirm delivery'}
          </span>
        </div>

        {/* Slider Button */}
        <div
          className="absolute top-2 left-2 w-12 h-12 bg-emerald-500 rounded-full flex items-center justify-center shadow-lg transition-transform"
          style={{ transform: `translateX(${sliderPosition}px)` }}
          onMouseDown={handleMouseDown}
          onTouchStart={handleTouchStart}
        >
          {isDelivering ? (
            <Check className="w-6 h-6 text-white" />
          ) : (
            <ChevronRight className="w-6 h-6 text-white" />
          )}
        </div>
      </div>

      <p className="text-center text-sm text-[#6E6E6E] mt-4">
        Slide the button to mark as delivered
      </p>
    </div>
  );
}

export default DriverLogistics;
