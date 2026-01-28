import { useState } from 'react';
import { ArrowLeft, Check, AlertCircle, Calendar as CalendarIcon } from 'lucide-react';
import { bouquets, addOns } from '../../data/mockData';
import type { CartItem } from './CustomerExperience';

interface ProductDetailProps {
  bouquet: typeof bouquets[0];
  onBack: () => void;
  onAddToCart: (cartItem: CartItem) => void;
}

function ProductDetail({ bouquet, onBack, onAddToCart }: ProductDetailProps) {
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [selectedAddOns, setSelectedAddOns] = useState<number[]>([]);
  const [quantity, setQuantity] = useState(1);
  const [dateError, setDateError] = useState(false);

  // Generate available dates (next 14 days)
  const generateDates = () => {
    const dates = [];
    const today = new Date();
    const cutoffHour = parseInt(bouquet.cutoffTime.split(':')[0]);
    const currentHour = today.getHours();
    
    for (let i = 0; i < 14; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      
      // Disable today if past cutoff time
      const isToday = i === 0;
      const isPastCutoff = isToday && currentHour >= cutoffHour;
      
      dates.push({
        date,
        disabled: isPastCutoff,
        label: isToday ? 'Today' : date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
      });
    }
    return dates;
  };

  const dates = generateDates();

  const toggleAddOn = (addOnId: number) => {
    setSelectedAddOns(prev => 
      prev.includes(addOnId) 
        ? prev.filter(id => id !== addOnId)
        : [...prev, addOnId]
    );
  };

  const calculateTotal = () => {
    const addOnsTotal = selectedAddOns.reduce((sum, id) => {
      const addOn = addOns.find(a => a.id === id);
      return sum + (addOn?.price || 0);
    }, 0);
    return (bouquet.price + addOnsTotal) * quantity;
  };

  const handleAddToCart = () => {
    if (!selectedDate) {
      setDateError(true);
      setTimeout(() => setDateError(false), 3000);
      return;
    }

    const selectedAddOnItems = addOns.filter(a => selectedAddOns.includes(a.id));
    
    onAddToCart({
      bouquet,
      quantity,
      deliveryDate: selectedDate,
      addOns: selectedAddOnItems
    });
  };

  const isAvailable = bouquet.available;

  return (
    <div className="min-h-screen bg-[#F6F7F3] pb-20">
      {/* Breadcrumb */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-[#6E6E6E] hover:text-[#2A2A2A] transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span className="text-sm font-medium">Back to shop</span>
        </button>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12">
          {/* Product Image */}
          <div className="relative">
            <div className="aspect-[4/5] rounded-[28px] overflow-hidden bg-white shadow-lg">
              <img
                src={bouquet.image}
                alt={bouquet.name}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="absolute top-4 left-4">
              <span className="px-4 py-2 bg-white/90 backdrop-blur-sm rounded-full text-sm font-medium text-[#2A2A2A]">
                {bouquet.occasion}
              </span>
            </div>
          </div>

          {/* Product Info */}
          <div className="lg:py-8">
            <h1 className="text-4xl md:text-5xl font-heading font-bold text-[#2A2A2A] mb-4">
              {bouquet.name}
            </h1>
            <p className="text-xl text-[#6E6E6E] mb-6">
              {bouquet.description}
            </p>

            {/* Price & Availability */}
            <div className="flex items-center gap-6 mb-8">
              <span className="text-4xl font-heading font-bold text-[#E57F84]">
                ${bouquet.price}
              </span>
              <div className={`flex items-center gap-2 px-4 py-2 rounded-full ${
                isAvailable 
                  ? 'bg-emerald-100 text-emerald-700' 
                  : 'bg-amber-100 text-amber-700'
              }`}>
                {isAvailable ? (
                  <>
                    <Check className="w-4 h-4" />
                    <span className="text-sm font-medium">Available</span>
                  </>
                ) : (
                  <>
                    <AlertCircle className="w-4 h-4" />
                    <span className="text-sm font-medium">Low Stock</span>
                  </>
                )}
              </div>
            </div>

            {/* Cutoff Time Notice */}
            <div className="bg-[#E8F2E8] rounded-2xl p-4 mb-8">
              <div className="flex items-start gap-3">
                <CalendarIcon className="w-5 h-5 text-[#8BA078] mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-[#2A2A2A]">
                    Order by {bouquet.cutoffTime} for same-day delivery
                  </p>
                  <p className="text-sm text-[#6E6E6E] mt-1">
                    Orders placed after cutoff will be delivered next business day
                  </p>
                </div>
              </div>
            </div>

            {/* Date Picker */}
            <div className="mb-8">
              <label className="block text-sm font-medium text-[#2A2A2A] mb-3">
                Select Delivery Date
                {dateError && (
                  <span className="ml-2 text-amber-600 font-normal">
                    Please select a date first
                  </span>
                )}
              </label>
              <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                {dates.map((dateInfo, index) => (
                  <button
                    key={index}
                    onClick={() => !dateInfo.disabled && setSelectedDate(dateInfo.date)}
                    disabled={dateInfo.disabled}
                    className={`p-3 rounded-xl text-sm font-medium transition-all ${
                      dateInfo.disabled
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        : selectedDate?.toDateString() === dateInfo.date.toDateString()
                        ? 'bg-[#E57F84] text-white'
                        : 'bg-white border border-[rgba(139,160,120,0.2)] text-[#2A2A2A] hover:border-[#8BA078]'
                    }`}
                  >
                    <div className="text-xs opacity-70">{dateInfo.label.split(' ')[0]}</div>
                    <div>{dateInfo.date.getDate()}</div>
                    {dateInfo.disabled && (
                      <div className="text-[10px] mt-1">Cutoff passed</div>
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Add-ons */}
            <div className="mb-8">
              <label className="block text-sm font-medium text-[#2A2A2A] mb-3">
                Add-ons (Optional)
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {addOns.map((addOn) => (
                  <button
                    key={addOn.id}
                    onClick={() => toggleAddOn(addOn.id)}
                    className={`p-4 rounded-xl border-2 transition-all text-left ${
                      selectedAddOns.includes(addOn.id)
                        ? 'border-[#E57F84] bg-[#E57F84]/5'
                        : 'border-[rgba(139,160,120,0.2)] bg-white hover:border-[#8BA078]'
                    }`}
                  >
                    <div className="text-2xl mb-2">{addOn.image}</div>
                    <div className="text-sm font-medium text-[#2A2A2A]">{addOn.name}</div>
                    <div className="text-sm text-[#E57F84] font-semibold">+${addOn.price}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Quantity */}
            <div className="mb-8">
              <label className="block text-sm font-medium text-[#2A2A2A] mb-3">
                Quantity
              </label>
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="w-10 h-10 rounded-full bg-white border border-[rgba(139,160,120,0.2)] flex items-center justify-center hover:border-[#8BA078] transition-colors"
                >
                  -
                </button>
                <span className="text-xl font-semibold w-8 text-center">{quantity}</span>
                <button
                  onClick={() => setQuantity(quantity + 1)}
                  className="w-10 h-10 rounded-full bg-white border border-[rgba(139,160,120,0.2)] flex items-center justify-center hover:border-[#8BA078] transition-colors"
                >
                  +
                </button>
              </div>
            </div>

            {/* Recipe Ingredients */}
            <div className="mb-8">
              <label className="block text-sm font-medium text-[#2A2A2A] mb-3">
                What's Included
              </label>
              <div className="bg-white rounded-2xl p-5">
                <ul className="space-y-2">
                  {bouquet.ingredients.map((ingredient, index) => (
                    <li key={index} className="flex items-center justify-between text-sm">
                      <span className="text-[#6E6E6E]">{ingredient.name}</span>
                      <span className="font-medium text-[#2A2A2A]">{ingredient.quantity} {ingredient.name.includes('Roses') || ingredient.name.includes('Peonies') || ingredient.name.includes('Lilies') || ingredient.name.includes('Sunflowers') || ingredient.name.includes('Tulips') || ingredient.name.includes('Daisies') || ingredient.name.includes('Carnations') || ingredient.name.includes('Gerberas') || ingredient.name.includes('Hyacinths') || ingredient.name.includes('Daffodils') || ingredient.name.includes('Alstroemeria') ? 'stems' : 'bunches'}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Total & CTA */}
            <div className="flex flex-col sm:flex-row items-center gap-6 pt-6 border-t border-[rgba(139,160,120,0.2)]">
              <div className="flex-1">
                <p className="text-sm text-[#6E6E6E]">Total</p>
                <p className="text-3xl font-heading font-bold text-[#2A2A2A]">
                  ${calculateTotal()}
                </p>
              </div>
              <button
                onClick={handleAddToCart}
                className="btn-primary w-full sm:w-auto text-lg px-8 py-4"
              >
                {selectedDate ? 'Add to Cart' : 'Select Delivery Date'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
