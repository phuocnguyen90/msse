// Bouquets data for Customer Experience
export const bouquets = [
  {
    id: 1,
    name: "Valentine's Romance",
    price: 89,
    image: "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&h=800&fit=crop",
    occasion: "Romance",
    description: "A stunning arrangement of red roses, pink peonies, and baby's breath.",
    ingredients: [
      { name: "Red Roses", quantity: 12 },
      { name: "Pink Peonies", quantity: 5 },
      { name: "Baby's Breath", quantity: 3 },
      { name: "Eucalyptus", quantity: 4 }
    ],
    available: true,
    cutoffTime: "14:00"
  },
  {
    id: 2,
    name: "Birthday Bliss",
    price: 68,
    image: "https://images.unsplash.com/photo-1563241527-3004b7be0ffd?w=600&h=800&fit=crop",
    occasion: "Birthday",
    description: "Bright sunflowers, daisies, and colorful gerberas to celebrate.",
    ingredients: [
      { name: "Sunflowers", quantity: 6 },
      { name: "Daisies", quantity: 8 },
      { name: "Gerberas", quantity: 4 },
      { name: "Greenery", quantity: 5 }
    ],
    available: true,
    cutoffTime: "12:00"
  },
  {
    id: 3,
    name: "Sympathy Whites",
    price: 95,
    image: "https://images.unsplash.com/photo-1487530811176-3780de880c2d?w=600&h=800&fit=crop",
    occasion: "Sympathy",
    description: "Elegant white lilies and roses for moments of remembrance.",
    ingredients: [
      { name: "White Lilies", quantity: 6 },
      { name: "White Roses", quantity: 8 },
      { name: "Carnations", quantity: 5 },
      { name: "Ferns", quantity: 6 }
    ],
    available: true,
    cutoffTime: "13:00"
  },
  {
    id: 4,
    name: "Spring Garden",
    price: 75,
    image: "https://images.unsplash.com/photo-1525310072745-f49212b5ac6d?w=600&h=800&fit=crop",
    occasion: "Just because",
    description: "A delightful mix of seasonal tulips, daffodils, and hyacinths.",
    ingredients: [
      { name: "Tulips", quantity: 10 },
      { name: "Daffodils", quantity: 6 },
      { name: "Hyacinths", quantity: 3 },
      { name: "Pussy Willow", quantity: 4 }
    ],
    available: true,
    cutoffTime: "14:00"
  },
  {
    id: 5,
    name: "Thank You Bouquet",
    price: 58,
    image: "https://images.unsplash.com/photo-1494972308805-463bc619d34e?w=600&h=800&fit=crop",
    occasion: "Thank you",
    description: "Soft pink carnations and alstroemeria to express gratitude.",
    ingredients: [
      { name: "Pink Carnations", quantity: 8 },
      { name: "Alstroemeria", quantity: 6 },
      { name: "Statice", quantity: 4 },
      { name: "Ruscus", quantity: 5 }
    ],
    available: true,
    cutoffTime: "14:00"
  },
  {
    id: 6,
    name: "Sunset Dreams",
    price: 82,
    image: "https://images.unsplash.com/photo-1508610048659-a06b669e3321?w=600&h=800&fit=crop",
    occasion: "Romance",
    description: "Warm oranges and peaches with roses and chrysanthemums.",
    ingredients: [
      { name: "Orange Roses", quantity: 8 },
      { name: "Chrysanthemums", quantity: 6 },
      { name: "Peach Carnations", quantity: 5 },
      { name: "Solidago", quantity: 4 }
    ],
    available: true,
    cutoffTime: "14:00"
  }
];

// Add-ons for checkout
export const addOns = [
  { id: 1, name: "Scented Candle", price: 24, image: "🕯️" },
  { id: 2, name: "Greeting Card", price: 6, image: "💌" },
  { id: 3, name: "Chocolate Box", price: 18, image: "🍫" },
  { id: 4, name: "Vase", price: 32, image: "🏺" },
  { id: 5, name: "Teddy Bear", price: 28, image: "🧸" },
  { id: 6, name: "Balloon", price: 8, image: "🎈" }
];

// Occasions
export const occasions = ["Birthday", "Romance", "Thank you", "Sympathy", "Just because"];

// Inventory data for Manager Dashboard
export const inventory = [
  { id: 1, name: "Red Roses", quantity: 45, unit: "stems", minLevel: 20, status: "good" },
  { id: 2, name: "Pink Peonies", quantity: 12, unit: "stems", minLevel: 15, status: "low" },
  { id: 3, name: "White Lilies", quantity: 28, unit: "stems", minLevel: 15, status: "good" },
  { id: 4, name: "Sunflowers", quantity: 8, unit: "stems", minLevel: 12, status: "low" },
  { id: 5, name: "Tulips", quantity: 60, unit: "stems", minLevel: 25, status: "good" },
  { id: 6, name: "Eucalyptus", quantity: 35, unit: "bunches", minLevel: 10, status: "good" },
  { id: 7, name: "Baby's Breath", quantity: 15, unit: "bunches", minLevel: 8, status: "good" },
  { id: 8, name: "Ferns", quantity: 10, unit: "bunches", minLevel: 12, status: "low" },
  { id: 9, name: "Daisies", quantity: 42, unit: "stems", minLevel: 20, status: "good" },
  { id: 10, name: "Carnations", quantity: 55, unit: "stems", minLevel: 20, status: "good" }
];

// Product recipes for Manager
export const recipes = [
  {
    id: 1,
    name: "Valentine's Romance",
    ingredients: [
      { name: "Red Roses", quantity: 12 },
      { name: "Pink Peonies", quantity: 5 },
      { name: "Baby's Breath", quantity: 3 },
      { name: "Eucalyptus", quantity: 4 }
    ]
  },
  {
    id: 2,
    name: "Birthday Bliss",
    ingredients: [
      { name: "Sunflowers", quantity: 6 },
      { name: "Daisies", quantity: 8 },
      { name: "Gerberas", quantity: 4 },
      { name: "Greenery", quantity: 5 }
    ]
  },
  {
    id: 3,
    name: "Sympathy Whites",
    ingredients: [
      { name: "White Lilies", quantity: 6 },
      { name: "White Roses", quantity: 8 },
      { name: "Carnations", quantity: 5 },
      { name: "Ferns", quantity: 6 }
    ]
  }
];

// Orders for Florist Production View
export const productionOrders = [
  {
    id: "ORD-2025-001",
    customer: "Sarah Johnson",
    bouquet: "Valentine's Romance",
    ingredients: [
      { name: "Red Roses", quantity: 12 },
      { name: "Pink Peonies", quantity: 5 },
      { name: "Baby's Breath", quantity: 3 },
      { name: "Eucalyptus", quantity: 4 }
    ],
    status: "to-make",
    priority: "high",
    deliveryTime: "14:00",
    note: "Please include extra ribbon"
  },
  {
    id: "ORD-2025-002",
    customer: "Michael Chen",
    bouquet: "Birthday Bliss",
    ingredients: [
      { name: "Sunflowers", quantity: 6 },
      { name: "Daisies", quantity: 8 },
      { name: "Gerberas", quantity: 4 },
      { name: "Greenery", quantity: 5 }
    ],
    status: "to-make",
    priority: "normal",
    deliveryTime: "15:30",
    note: ""
  },
  {
    id: "ORD-2025-003",
    customer: "Emma Williams",
    bouquet: "Spring Garden",
    ingredients: [
      { name: "Tulips", quantity: 10 },
      { name: "Daffodils", quantity: 6 },
      { name: "Hyacinths", quantity: 3 },
      { name: "Pussy Willow", quantity: 4 }
    ],
    status: "in-progress",
    priority: "normal",
    deliveryTime: "16:00",
    note: "Allergic to lilies - confirmed OK"
  },
  {
    id: "ORD-2025-004",
    customer: "David Brown",
    bouquet: "Sympathy Whites",
    ingredients: [
      { name: "White Lilies", quantity: 6 },
      { name: "White Roses", quantity: 8 },
      { name: "Carnations", quantity: 5 },
      { name: "Ferns", quantity: 6 }
    ],
    status: "to-make",
    priority: "high",
    deliveryTime: "13:00",
    note: "Funeral delivery - be discreet"
  },
  {
    id: "ORD-2025-005",
    customer: "Lisa Garcia",
    bouquet: "Thank You Bouquet",
    ingredients: [
      { name: "Pink Carnations", quantity: 8 },
      { name: "Alstroemeria", quantity: 6 },
      { name: "Statice", quantity: 4 },
      { name: "Ruscus", quantity: 5 }
    ],
    status: "in-progress",
    priority: "normal",
    deliveryTime: "17:00",
    note: ""
  }
];

// Delivery orders for Driver View
export const deliveryOrders = [
  {
    id: "ORD-2025-001",
    recipient: "Sarah Johnson",
    address: "123 Maple Street, Apt 4B",
    phone: "(555) 123-4567",
    instructions: "Gate code: 4729. Leave with doorman.",
    zone: "Downtown",
    status: "ready",
    bouquet: "Valentine's Romance"
  },
  {
    id: "ORD-2025-002",
    recipient: "Michael Chen",
    address: "456 Oak Avenue, Suite 200",
    phone: "(555) 234-5678",
    instructions: "Office building. Call upon arrival.",
    zone: "Midtown",
    status: "ready",
    bouquet: "Birthday Bliss"
  },
  {
    id: "ORD-2025-003",
    recipient: "Emma Williams",
    address: "789 Pine Road",
    phone: "(555) 345-6789",
    instructions: "Ring doorbell. Dog may bark.",
    zone: "Uptown",
    status: "ready",
    bouquet: "Spring Garden"
  },
  {
    id: "ORD-2025-005",
    recipient: "Lisa Garcia",
    address: "321 Elm Boulevard",
    phone: "(555) 456-7890",
    instructions: "Side entrance. Text when arrived.",
    zone: "Downtown",
    status: "ready",
    bouquet: "Thank You Bouquet"
  }
];

// Manager dashboard metrics
export const dashboardMetrics = {
  totalSales: 2847,
  ordersToday: 24,
  pendingOrders: 8,
  lowStockItems: 3,
  revenueToday: 1856,
  revenueWeek: 12450
};
