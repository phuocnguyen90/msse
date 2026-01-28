import { useState } from 'react';
import { X, Check, MapPin, Store, CreditCard, User, ChevronRight, Truck, Gift } from 'lucide-react';
import type { CartItem } from './CustomerExperience';
import { addOns } from '../../data/mockData';

interface CheckoutModalProps {
  cart: CartItem;
  onClose: () => void;
  onComplete: () => void;
}

type CheckoutStep = 1 | 2 | 3 | 4;
type DeliveryType = 'delivery' | 'pickup' | null;

function CheckoutModal({ cart, onClose, onComplete }: CheckoutModalProps) {
  const [currentStep, setCurrentStep] = useState<CheckoutStep>(1);
  const [deliveryType, setDeliveryType] = useState<DeliveryType>(null);
  const [address, setAddress] = useState({
    street: '',
    city: '',
    zip: '',
    phone: ''
  });
  const [selectedAddOns, setSelectedAddOns] = useState(cart.addOns.map(a => a.id));
  const [isGuest, setIsGuest] = useState(true);
  const [paymentInfo, setPaymentInfo] = useState({
    cardNumber: '',
    expiry: '',
    cvv: '',
    name: ''
  });

  const steps = [
    { number: 1, title: 'Delivery', icon: Truck },
    { number: 2, title: 'Address', icon: MapPin },
    { number: 3, title: 'Add-ons', icon: Gift },
    { number: 4, title: 'Payment', icon: CreditCard }
  ];

  const calculateTotal = () => {
    const addOnsTotal = selectedAddOns.reduce((sum, id) => {
      const addOn = addOns.find(a => a.id === id);
      return sum + (addOn?.price || 0);
    }, 0);
    return (cart.bouquet.price + addOnsTotal) * cart.quantity;
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return deliveryType !== null;
      case 2:
        return deliveryType === 'pickup' || (address.street && address.city && address.zip);
      case 3:
        return true;
      case 4:
        return isGuest || (paymentInfo.cardNumber && paymentInfo.expiry && paymentInfo.cvv);
      default:
        return false;
    }
  };

  const handleNext = () => {
    if (currentStep < 4) {
      setCurrentStep((prev) => (prev + 1) as CheckoutStep);
    } else {
      onComplete();
    }
  };

  const toggleAddOn = (addOnId: number) => {
    setSelectedAddOns(prev => 
      prev.includes(addOnId) 
        ? prev.filter(id => id !== addOnId)
        : [...prev, addOnId]
    );
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative bg-white rounded-[28px] w-full max-w-2xl max-h-[90vh] overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-[rgba(139,160,120,0.15)]">
          <h2 className="text-2xl font-heading font-bold text-[#2A2A2A]">Checkout</h2>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-[#F6F7F3] rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-[#6E6E6E]" />
          </button>
        </div>

        {/* Progress Steps */}
        <div className="flex items-center justify-center gap-2 p-6 bg-[#F6F7F3]">
          {steps.map((step, index) => (
            <div key={step.number} className="flex items-center">
              <div className={`flex items-center gap-2 px-4 py-2 rounded-full ${
                currentStep === step.number
                  ? 'bg-[#E57F84] text-white'
                  : currentStep > step.number
                  ? 'bg-emerald-100 text-emerald-700'
                  : 'bg-white text-[#6E6E6E]'
              }`}>
                <step.icon className="w-4 h-4" />
                <span className="text-sm font-medium hidden sm:inline">{step.title}</span>
                {currentStep > step.number && (
                  <Check className="w-4 h-4" />
                )}
              </div>
              {index < steps.length - 1 && (
                <ChevronRight className="w-4 h-4 text-[#6E6E6E] mx-1" />
              )}
            </div>
          ))}
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[50vh]">
          {/* Step 1: Delivery Type */}
          {currentStep === 1 && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-[#2A2A2A] mb-4">
                How would you like to receive your order?
              </h3>
              <button
                onClick={() => setDeliveryType('delivery')}
                className={`w-full p-6 rounded-2xl border-2 transition-all flex items-center gap-4 ${
                  deliveryType === 'delivery'
                    ? 'border-[#E57F84] bg-[#E57F84]/5'
                    : 'border-[rgba(139,160,120,0.2)] hover:border-[#8BA078]'
                }`}
              >
                <div className={`w-14 h-14 rounded-xl flex items-center justify-center ${
                  deliveryType === 'delivery' ? 'bg-[#E57F84]' : 'bg-[#E8F2E8]'
                }`}>
                  <Truck className={`w-7 h-7 ${deliveryType === 'delivery' ? 'text-white' : 'text-[#8BA078]'}`} />
                </div>
                <div className="text-left flex-1">
                  <h4 className="font-semibold text-[#2A2A2A]">Delivery</h4>
                  <p className="text-sm text-[#6E6E6E]">Same-day delivery to your door</p>
                </div>
                {deliveryType === 'delivery' && <Check className="w-6 h-6 text-[#E57F84]" />}
              </button>

              <button
                onClick={() => setDeliveryType('pickup')}
                className={`w-full p-6 rounded-2xl border-2 transition-all flex items-center gap-4 ${
                  deliveryType === 'pickup'
                    ? 'border-[#E57F84] bg-[#E57F84]/5'
                    : 'border-[rgba(139,160,120,0.2)] hover:border-[#8BA078]'
                }`}
              >
                <div className={`w-14 h-14 rounded-xl flex items-center justify-center ${
                  deliveryType === 'pickup' ? 'bg-[#E57F84]' : 'bg-[#E8F2E8]'
                }`}>
                  <Store className={`w-7 h-7 ${deliveryType === 'pickup' ? 'text-white' : 'text-[#8BA078]'}`} />
                </div>
                <div className="text-left flex-1">
                  <h4 className="font-semibold text-[#2A2A2A]">Studio Pickup</h4>
                  <p className="text-sm text-[#6E6E6E]">Pick up at 123 Bloom Street</p>
                </div>
                {deliveryType === 'pickup' && <Check className="w-6 h-6 text-[#E57F84]" />}
              </button>
            </div>
          )}

          {/* Step 2: Address */}
          {currentStep === 2 && (
            <div className="space-y-4">
              {deliveryType === 'pickup' ? (
                <div className="text-center py-8">
                  <div className="w-20 h-20 bg-[#E8F2E8] rounded-full flex items-center justify-center mx-auto mb-4">
                    <Store className="w-10 h-10 text-[#8BA078]" />
                  </div>
                  <h3 className="text-xl font-semibold text-[#2A2A2A] mb-2">
                    Studio Pickup
                  </h3>
                  <p className="text-[#6E6E6E] mb-4">
                    123 Bloom Street, Plant City
                  </p>
                  <div className="bg-[#F6F7F3] rounded-xl p-4 inline-block">
                    <p className="text-sm text-[#6E6E6E]">
                      Mon–Fri: 8am–6pm<br />
                      Sat: 9am–4pm
                    </p>
                  </div>
                </div>
              ) : (
                <>
                  <h3 className="text-lg font-semibold text-[#2A2A2A] mb-4">
                    Enter delivery address
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-[#2A2A2A] mb-2">
                        Street Address
                      </label>
                      <input
                        type="text"
                        value={address.street}
                        onChange={(e) => setAddress({ ...address, street: e.target.value })}
                        placeholder="123 Main Street, Apt 4B"
                        className="w-full px-4 py-3 rounded-xl border border-[rgba(139,160,120,0.2)] focus:border-[#E57F84] focus:ring-2 focus:ring-[#E57F84]/20 outline-none transition-all"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-[#2A2A2A] mb-2">
                          City
                        </label>
                        <input
                          type="text"
                          value={address.city}
                          onChange={(e) => setAddress({ ...address, city: e.target.value })}
                          placeholder="Plant City"
                          className="w-full px-4 py-3 rounded-xl border border-[rgba(139,160,120,0.2)] focus:border-[#E57F84] focus:ring-2 focus:ring-[#E57F84]/20 outline-none transition-all"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-[#2A2A2A] mb-2">
                          ZIP Code
                        </label>
                        <input
                          type="text"
                          value={address.zip}
                          onChange={(e) => setAddress({ ...address, zip: e.target.value })}
                          placeholder="12345"
                          className="w-full px-4 py-3 rounded-xl border border-[rgba(139,160,120,0.2)] focus:border-[#E57F84] focus:ring-2 focus:ring-[#E57F84]/20 outline-none transition-all"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-[#2A2A2A] mb-2">
                        Phone Number
                      </label>
                      <input
                        type="tel"
                        value={address.phone}
                        onChange={(e) => setAddress({ ...address, phone: e.target.value })}
                        placeholder="(555) 123-4567"
                        className="w-full px-4 py-3 rounded-xl border border-[rgba(139,160,120,0.2)] focus:border-[#E57F84] focus:ring-2 focus:ring-[#E57F84]/20 outline-none transition-all"
                      />
                    </div>
                  </div>
                </>
              )}
            </div>
          )}

          {/* Step 3: Add-ons */}
          {currentStep === 3 && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-[#2A2A2A] mb-4">
                Enhance your gift with add-ons
              </h3>
              <div className="grid grid-cols-2 gap-3">
                {addOns.map((addOn) => (
                  <button
                    key={addOn.id}
                    onClick={() => toggleAddOn(addOn.id)}
                    className={`p-4 rounded-xl border-2 transition-all text-left ${
                      selectedAddOns.includes(addOn.id)
                        ? 'border-[#E57F84] bg-[#E57F84]/5'
                        : 'border-[rgba(139,160,120,0.2)] hover:border-[#8BA078]'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="text-2xl mb-2">{addOn.image}</div>
                        <div className="text-sm font-medium text-[#2A2A2A]">{addOn.name}</div>
                        <div className="text-sm text-[#E57F84] font-semibold">${addOn.price}</div>
                      </div>
                      {selectedAddOns.includes(addOn.id) && (
                        <Check className="w-5 h-5 text-[#E57F84]" />
                      )}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Step 4: Payment */}
          {currentStep === 4 && (
            <div className="space-y-4">
              {/* Guest or Login Toggle */}
              <div className="flex gap-4 mb-6">
                <button
                  onClick={() => setIsGuest(true)}
                  className={`flex-1 py-3 px-4 rounded-xl border-2 transition-all ${
                    isGuest
                      ? 'border-[#E57F84] bg-[#E57F84]/5'
                      : 'border-[rgba(139,160,120,0.2)]'
                  }`}
                >
                  <div className="flex items-center justify-center gap-2">
                    <User className="w-4 h-4" />
                    <span className="font-medium">Guest Checkout</span>
                  </div>
                </button>
                <button
                  onClick={() => setIsGuest(false)}
                  className={`flex-1 py-3 px-4 rounded-xl border-2 transition-all ${
                    !isGuest
                      ? 'border-[#E57F84] bg-[#E57F84]/5'
                      : 'border-[rgba(139,160,120,0.2)]'
                  }`}
                >
                  <span className="font-medium">Login</span>
                </button>
              </div>

              {isGuest ? (
                <div className="bg-[#E8F2E8] rounded-xl p-4">
                  <p className="text-sm text-[#2A2A2A]">
                    You'll receive an order confirmation email. No account needed!
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-[#2A2A2A] mb-2">
                      Card Number
                    </label>
                    <input
                      type="text"
                      value={paymentInfo.cardNumber}
                      onChange={(e) => setPaymentInfo({ ...paymentInfo, cardNumber: e.target.value })}
                      placeholder="1234 5678 9012 3456"
                      className="w-full px-4 py-3 rounded-xl border border-[rgba(139,160,120,0.2)] focus:border-[#E57F84] focus:ring-2 focus:ring-[#E57F84]/20 outline-none transition-all"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-[#2A2A2A] mb-2">
                        Expiry
                      </label>
                      <input
                        type="text"
                        value={paymentInfo.expiry}
                        onChange={(e) => setPaymentInfo({ ...paymentInfo, expiry: e.target.value })}
                        placeholder="MM/YY"
                        className="w-full px-4 py-3 rounded-xl border border-[rgba(139,160,120,0.2)] focus:border-[#E57F84] focus:ring-2 focus:ring-[#E57F84]/20 outline-none transition-all"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-[#2A2A2A] mb-2">
                        CVV
                      </label>
                      <input
                        type="text"
                        value={paymentInfo.cvv}
                        onChange={(e) => setPaymentInfo({ ...paymentInfo, cvv: e.target.value })}
                        placeholder="123"
                        className="w-full px-4 py-3 rounded-xl border border-[rgba(139,160,120,0.2)] focus:border-[#E57F84] focus:ring-2 focus:ring-[#E57F84]/20 outline-none transition-all"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-[#2A2A2A] mb-2">
                      Cardholder Name
                    </label>
                    <input
                      type="text"
                      value={paymentInfo.name}
                      onChange={(e) => setPaymentInfo({ ...paymentInfo, name: e.target.value })}
                      placeholder="John Doe"
                      className="w-full px-4 py-3 rounded-xl border border-[rgba(139,160,120,0.2)] focus:border-[#E57F84] focus:ring-2 focus:ring-[#E57F84]/20 outline-none transition-all"
                    />
                  </div>
                </div>
              )}

              {/* Order Summary */}
              <div className="border-t border-[rgba(139,160,120,0.2)] pt-4 mt-4">
                <h4 className="font-semibold text-[#2A2A2A] mb-3">Order Summary</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-[#6E6E6E]">{cart.bouquet.name} x{cart.quantity}</span>
                    <span className="font-medium">${cart.bouquet.price * cart.quantity}</span>
                  </div>
                  {selectedAddOns.length > 0 && (
                    <div className="flex justify-between">
                      <span className="text-[#6E6E6E]">Add-ons</span>
                      <span className="font-medium">
                        +${selectedAddOns.reduce((sum, id) => {
                          const addOn = addOns.find(a => a.id === id);
                          return sum + (addOn?.price || 0);
                        }, 0)}
                      </span>
                    </div>
                  )}
                  <div className="flex justify-between pt-2 border-t border-[rgba(139,160,120,0.15)]">
                    <span className="font-semibold text-[#2A2A2A]">Total</span>
                    <span className="font-bold text-[#E57F84] text-lg">${calculateTotal()}</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-[rgba(139,160,120,0.15)] bg-[#F6F7F3]">
          <div className="flex items-center justify-between">
            {currentStep > 1 ? (
              <button
                onClick={() => setCurrentStep((prev) => (prev - 1) as CheckoutStep)}
                className="px-6 py-3 text-[#6E6E6E] font-medium hover:text-[#2A2A2A] transition-colors"
              >
                Back
              </button>
            ) : (
              <div />
            )}
            <button
              onClick={handleNext}
              disabled={!canProceed()}
              className={`btn-primary ${!canProceed() ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {currentStep === 4 ? 'Place Order' : 'Continue'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CheckoutModal;
