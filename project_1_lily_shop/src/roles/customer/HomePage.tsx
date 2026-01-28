import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { ArrowRight, Heart, Gift, Sparkles, Flower2 } from 'lucide-react';
import { bouquets, occasions } from '../../data/mockData';

gsap.registerPlugin(ScrollTrigger);

interface HomePageProps {
  onBouquetClick: (bouquet: typeof bouquets[0]) => void;
}

function HomePage({ onBouquetClick }: HomePageProps) {
  const heroRef = useRef<HTMLDivElement>(null);
  const stepsRef = useRef<HTMLDivElement>(null);
  const gridRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Hero animation
      gsap.fromTo('.hero-content',
        { opacity: 0, x: -60 },
        { opacity: 1, x: 0, duration: 1, ease: 'power3.out' }
      );

      gsap.fromTo('.hero-image',
        { scale: 1.1, opacity: 0 },
        { scale: 1, opacity: 1, duration: 1.2, ease: 'power2.out' }
      );

      // Steps animation
      gsap.fromTo('.step-card',
        { opacity: 0, y: 40 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.15,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: stepsRef.current,
            start: 'top 80%',
            toggleActions: 'play none none reverse'
          }
        }
      );

      // Grid animation
      gsap.fromTo('.bouquet-card',
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          stagger: 0.1,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: gridRef.current,
            start: 'top 80%',
            toggleActions: 'play none none reverse'
          }
        }
      );
    });

    return () => ctx.revert();
  }, []);

  return (
    <div className="overflow-hidden">
      {/* Hero Section */}
      <section ref={heroRef} className="relative min-h-[90vh] flex items-center">
        {/* Background Image */}
        <div className="absolute inset-0 z-0">
          <div className="hero-image absolute inset-0">
            <img
              src="https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1920&h=1080&fit=crop"
              alt="Beautiful bouquet"
              className="w-full h-full object-cover"
            />
          </div>
          {/* Gradient Overlay */}
          <div 
            className="absolute inset-0"
            style={{
              background: 'linear-gradient(90deg, rgba(246,247,243,0.95) 0%, rgba(246,247,243,0.75) 45%, rgba(246,247,243,0) 100%)'
            }}
          />
        </div>

        {/* Hero Content */}
        <div className="hero-content relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="max-w-xl">
            <span className="inline-block px-4 py-2 bg-[#E57F84]/10 text-[#E57F84] rounded-full text-sm font-medium mb-6">
              💝 Valentine's Collection Available
            </span>
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-heading font-bold text-[#2A2A2A] leading-[0.95] mb-6">
              Fresh flowers,<br />
              <span className="text-[#E57F84]">delivered same day.</span>
            </h1>
            <p className="text-lg text-[#6E6E6E] mb-8 font-body leading-relaxed">
              Hand-tied bouquets from our studio to your door—crafted with seasonal stems and delivered with love.
            </p>
            <div className="flex flex-wrap gap-4">
              <button className="btn-primary flex items-center gap-2">
                Order for Valentine's
                <ArrowRight className="w-4 h-4" />
              </button>
              <button className="px-6 py-3 border-2 border-[#2A2A2A] text-[#2A2A2A] rounded-full font-medium hover:bg-[#2A2A2A] hover:text-white transition-all">
                See the Collection
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section ref={stepsRef} className="py-20 bg-[#F6F7F3]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-heading font-bold text-[#2A2A2A] mb-4">
              Three simple steps
            </h2>
            <p className="text-[#6E6E6E] text-lg">
              From selection to delivery, we've made it easy
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Flower2,
                title: 'Choose',
                description: 'Browse bouquets by occasion, mood, or color. Find the perfect match for any moment.',
                step: '01'
              },
              {
                icon: Sparkles,
                title: 'Personalize',
                description: 'Add a note, swap the vase, or build your own custom arrangement.',
                step: '02'
              },
              {
                icon: Gift,
                title: 'Receive',
                description: 'Same-day delivery or pickup from our studio. Freshness guaranteed.',
                step: '03'
              }
            ].map((step, index) => (
              <div
                key={index}
                className="step-card card-mint p-8 relative group hover:shadow-lg transition-all duration-300"
              >
                <span className="absolute top-4 right-4 text-6xl font-heading font-bold text-[#8BA078]/10">
                  {step.step}
                </span>
                <div className="w-14 h-14 bg-[#E57F84]/10 rounded-2xl flex items-center justify-center mb-6">
                  <step.icon className="w-7 h-7 text-[#E57F84]" />
                </div>
                <h3 className="text-2xl font-heading font-semibold text-[#2A2A2A] mb-3">
                  {step.title}
                </h3>
                <p className="text-[#6E6E6E] font-body">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Browse by Occasion */}
      <section className="py-20 bg-white/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between mb-12">
            <div>
              <h2 className="text-4xl md:text-5xl font-heading font-bold text-[#2A2A2A] mb-4">
                Browse by Occasion
              </h2>
              <p className="text-[#6E6E6E] text-lg max-w-xl">
                From birthdays to quiet thank-yous—choose a mood and we'll handle the rest.
              </p>
            </div>
          </div>

          {/* Occasion Chips */}
          <div className="flex flex-wrap gap-3 mb-12">
            {occasions.map((occasion, index) => (
              <button
                key={index}
                className="px-5 py-2.5 bg-white border border-[rgba(139,160,120,0.2)] rounded-full text-sm font-medium text-[#2A2A2A] hover:bg-[#E8F2E8] hover:border-[#8BA078] transition-all"
              >
                {occasion}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Fresh Seasonal Picks Grid */}
      <section ref={gridRef} className="py-20 bg-[#F6F7F3]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-12">
            <h2 className="text-4xl md:text-5xl font-heading font-bold text-[#2A2A2A]">
              Fresh Seasonal Picks
            </h2>
            <button className="hidden md:flex items-center gap-2 text-[#E57F84] font-medium hover:underline">
              View all bouquets
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {bouquets.map((bouquet) => (
              <div
                key={bouquet.id}
                onClick={() => onBouquetClick(bouquet)}
                className="bouquet-card group bg-white rounded-[28px] overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 cursor-pointer"
              >
                <div className="relative aspect-[4/5] overflow-hidden">
                  <img
                    src={bouquet.image}
                    alt={bouquet.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute top-4 left-4">
                    <span className="px-3 py-1 bg-white/90 backdrop-blur-sm rounded-full text-xs font-medium text-[#2A2A2A]">
                      {bouquet.occasion}
                    </span>
                  </div>
                  <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
                <div className="p-6">
                  <h3 className="text-xl font-heading font-semibold text-[#2A2A2A] mb-2">
                    {bouquet.name}
                  </h3>
                  <p className="text-[#6E6E6E] text-sm mb-4 line-clamp-2">
                    {bouquet.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-heading font-bold text-[#E57F84]">
                      ${bouquet.price}
                    </span>
                    <button className="w-10 h-10 bg-[#E8F2E8] rounded-full flex items-center justify-center group-hover:bg-[#E57F84] group-hover:text-white transition-colors">
                      <Heart className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-8 text-center md:hidden">
            <button className="inline-flex items-center gap-2 text-[#E57F84] font-medium">
              View all bouquets
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </section>

      {/* Same Day Delivery CTA */}
      <section className="py-20 bg-[#E8F2E8]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row items-center gap-12">
            <div className="flex-1 text-center lg:text-left">
              <h2 className="text-4xl md:text-5xl lg:text-6xl font-heading font-bold text-[#2A2A2A] mb-6">
                Order by 2pm
              </h2>
              <p className="text-xl text-[#6E6E6E] mb-4">
                For same-day delivery across the city.
              </p>
              <p className="text-[#6E6E6E] mb-8">
                We prepare every bouquet fresh each morning. Order early for the best selection.
              </p>
              <div className="flex flex-wrap gap-4 justify-center lg:justify-start">
                <button className="btn-primary">
                  Check Delivery Zones
                </button>
                <button className="px-6 py-3 text-[#6E6E6E] font-medium hover:text-[#2A2A2A] transition-colors">
                  Studio Pickup Hours
                </button>
              </div>
            </div>
            <div className="flex-1">
              <img
                src="https://images.unsplash.com/photo-1562690868-60bbe7293e94?w=800&h=600&fit=crop"
                alt="Florist at work"
                className="rounded-[28px] shadow-2xl w-full"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-[#2A2A2A] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🌸</span>
              <span className="font-heading font-semibold text-xl">Lily's Florist</span>
            </div>
            <p className="text-white/60 text-sm">
              © 2025 Lily's Florist. Fresh flowers, delivered with care.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default HomePage;
