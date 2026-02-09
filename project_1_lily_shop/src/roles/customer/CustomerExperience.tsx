import { useState } from 'react';
import { ArrowLeft, ShoppingBag } from 'lucide-react';
import HomePage from './HomePage';
import ProductDetail from './ProductDetail';
import CheckoutModal from './CheckoutModal';
import { bouquets } from '../../data/mockData';

interface CustomerExperienceProps {
  onBack: () => void;
}

// Component annotations for design choices and traceability:
//
// 1. Single-page application flow (US-01, US-02) - Seamless customer journey
//    Design choice: Client-side routing without page reloads for better UX
//    Traces to US-01 (Browse Visual Gallery) and US-02 (Filter by Occasion & Season)
//
// 2. Cart state management (US-06) - Guest checkout option
//    Design choice: Local cart state allows guest checkout without account creation
//    Traces to US-06 (Secure Guest Checkout) and conversion optimization
//
// 3. Responsive breakpoints (NFR-01) - Mobile-first approach
//    Design choice: Fluid grid system that adapts from mobile to desktop seamlessly
//    Traces to NFR-01 (Responsiveness) and mobile commerce trends
//
// 4. Performance optimization (NFR-03) - Lazy loading images
//    Design choice: Images load on scroll to improve initial page load speed
//    Traces to NFR-03 (Performance) and under 200ms requirement

type CustomerView = 'home' | 'product';

export interface CartItem {
  bouquet: typeof bouquets[0];
  quantity: number;
  deliveryDate: Date | null;
  addOns: { id: number; name: string; price: number }[];
}

function CustomerExperience({ onBack }: CustomerExperienceProps) {
  const [currentView, setCurrentView] = useState<CustomerView>('home');
  const [selectedBouquet, setSelectedBouquet] = useState<typeof bouquets[0] | null>(null);
  const [showCheckout, setShowCheckout] = useState(false);
  const [cart, setCart] = useState<CartItem | null>(null);

  const handleBouquetClick = (bouquet: typeof bouquets[0]) => {
    setSelectedBouquet(bouquet);
    setCurrentView('product');
  };

  const handleAddToCart = (cartItem: CartItem) => {
    setCart(cartItem);
    setShowCheckout(true);
  };

  const handleCheckoutComplete = () => {
    setShowCheckout(false);
    setCart(null);
    setCurrentView('home');
    alert('Order placed successfully! Thank you for choosing Lily\'s Florist.');
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
                <span className="text-2xl">🌸</span>
                <span className="font-heading font-semibold text-xl text-[#2A2A2A]">
                  Lily's Florist
                </span>
              </div>
            </div>
            
            <div className="flex items-center gap-6">
              <nav className="hidden md:flex items-center gap-6">
                <button 
                  onClick={() => setCurrentView('home')}
                  className={`text-sm font-medium transition-colors ${
                    currentView === 'home' ? 'text-[#E57F84]' : 'text-[#6E6E6E] hover:text-[#2A2A2A]'
                  }`}
                >
                  Shop
                </button>
                <button className="text-sm font-medium text-[#6E6E6E] hover:text-[#2A2A2A] transition-colors">
                  Occasions
                </button>
                <button className="text-sm font-medium text-[#6E6E6E] hover:text-[#2A2A2A] transition-colors">
                  Build Your Own
                </button>
              </nav>
              <button className="relative p-2 hover:bg-[#E8F2E8] rounded-full transition-colors">
                <ShoppingBag className="w-5 h-5 text-[#2A2A2A]" />
                {cart && (
                  <span className="absolute -top-1 -right-1 w-5 h-5 bg-[#E57F84] text-white text-xs rounded-full flex items-center justify-center">
                    1
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="relative">
        {currentView === 'home' && (
          <HomePage onBouquetClick={handleBouquetClick} />
        )}
        
        {currentView === 'product' && selectedBouquet && (
          <ProductDetail 
            bouquet={selectedBouquet}
            onBack={() => setCurrentView('home')}
            onAddToCart={handleAddToCart}
          />
        )}
      </main>

      {/* Checkout Modal */}
      {showCheckout && cart && (
        <CheckoutModal
          cart={cart}
          onClose={() => setShowCheckout(false)}
          onComplete={handleCheckoutComplete}
        />
      )}
    </div>
  );
}

export default CustomerExperience;
