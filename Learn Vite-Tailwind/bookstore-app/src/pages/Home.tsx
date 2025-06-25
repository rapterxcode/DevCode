import React, { useState, useEffect, useRef } from 'react';

const Home: React.FC = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [mobileDropdownOpen, setMobileDropdownOpen] = useState<string | null>(null);

  // Refs for smooth scrolling
  const heroRef = useRef<HTMLDivElement>(null);
  const featuredRef = useRef<HTMLDivElement>(null);
  const newReleasesRef = useRef<HTMLDivElement>(null);
  const categoriesRef = useRef<HTMLDivElement>(null);
  const whyChooseRef = useRef<HTMLDivElement>(null);
  const ctaRef = useRef<HTMLDivElement>(null);

  // Dropdown menu data
  const dropdownMenus = {
    menu: {
      title: "Menu",
      items: [
        { 
          name: "Books", 
          description: "Explore our collection",
          icon: "📚",
          action: () => scrollToSection(featuredRef),
          subItems: [
            { name: "Featured Books", action: () => scrollToSection(featuredRef) },
            { name: "New Releases", action: () => scrollToSection(newReleasesRef) },
            { name: "Bestsellers", action: () => scrollToSection(featuredRef) },
            { name: "Coming Soon", action: () => scrollToSection(newReleasesRef) }
          ]
        },
        { 
          name: "Categories", 
          description: "Browse by genre",
          icon: "📖",
          action: () => scrollToSection(categoriesRef),
          subItems: [
            { name: "Fiction", action: () => scrollToSection(categoriesRef) },
            { name: "Non-Fiction", action: () => scrollToSection(categoriesRef) },
            { name: "Science Fiction", action: () => scrollToSection(categoriesRef) },
            { name: "Mystery & Thriller", action: () => scrollToSection(categoriesRef) },
            { name: "Romance", action: () => scrollToSection(categoriesRef) },
            { name: "Biography", action: () => scrollToSection(categoriesRef) }
          ]
        },
        { 
          name: "Services", 
          description: "Additional services",
          icon: "🎯",
          action: () => scrollToSection(whyChooseRef),
          subItems: [
            { name: "Book Clubs", action: () => scrollToSection(whyChooseRef) },
            { name: "Author Events", action: () => scrollToSection(whyChooseRef) },
            { name: "Reading Lists", action: () => scrollToSection(whyChooseRef) },
            { name: "Gift Cards", action: () => scrollToSection(whyChooseRef) }
          ]
        },
        { 
          name: "About", 
          description: "Learn more about us",
          icon: "ℹ️",
          action: () => scrollToSection(whyChooseRef),
          subItems: [
            { name: "Why Choose Us", action: () => scrollToSection(whyChooseRef) },
            { name: "Our Story", action: () => scrollToSection(whyChooseRef) },
            { name: "Join Us", action: () => scrollToSection(ctaRef) },
            { name: "Contact", action: () => scrollToSection(ctaRef) }
          ]
        }
      ]
    }
  };

  // Smooth scroll function
  const scrollToSection = (ref: React.RefObject<HTMLDivElement | null>) => {
    ref.current?.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
    setActiveDropdown(null); // Close dropdown after navigation
  };

  // Auto-slide functionality
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // Animation on mount
  useEffect(() => {
    setIsVisible(true);
  }, []);

  // Add CSS animations for image carousel
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes fadeInOut {
        0%, 25% { opacity: 1; }
        33%, 100% { opacity: 0; }
      }
      @keyframes pulse {
        0%, 25% { opacity: 1; transform: scale(1.25); }
        33%, 100% { opacity: 0.5; transform: scale(1); }
      }
    `;
    document.head.appendChild(style);
    return () => {
      document.head.removeChild(style);
    };
  }, []);

  // Helper function to get image from array
  const getBookImage = (imageArray: string[], index: number = 0) => {
    return imageArray[index] || imageArray[0] || '/default-book-cover.jpg';
  };

  // Mock data for featured books
  const featuredBooks = [
    { 
      id: 1, 
      title: "The Seven Husbands of Evelyn Hugo", 
      author: "Taylor Jenkins Reid", 
      genre: "Fiction",
      price: 24.99, 
      originalPrice: 32.99, 
      image: [
        "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=600&fit=crop", 
        "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=600&fit=crop&flip=h",
        "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=600&fit=crop&flip=v"
      ], 
      rating: 4.8,
      description: "A captivating novel about a reclusive Hollywood icon who finally decides to tell her story to a young journalist.",
      color: "from-purple-500 to-pink-500"
    },
    { 
      id: 2, 
      title: "Atomic Habits", 
      author: "James Clear", 
      genre: "Self-Help",
      price: 18.99, 
      originalPrice: 24.99, 
      image: [
        "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400&h=600&fit=crop",
        "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400&h=600&fit=crop&flip=h"
      ], 
      rating: 4.9,
      description: "An easy & proven way to build good habits & break bad ones. Transform your life with tiny changes.",
      color: "from-blue-500 to-cyan-500"
    },
    { 
      id: 3, 
      title: "Where the Crawdads Sing", 
      author: "Delia Owens", 
      genre: "Mystery",
      price: 22.99, 
      originalPrice: 28.99, 
      image: [
        "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=400&h=600&fit=crop", 
        "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=400&h=600&fit=crop&flip=v",
        "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=400&h=600&fit=crop&flip=h"
      ], 
      rating: 4.7,
      description: "A beautiful coming-of-age story and murder mystery set in the marshlands of North Carolina.",
      color: "from-green-500 to-emerald-500"
    },
    { 
      id: 4, 
      title: "The Silent Patient", 
      author: "Alex Michaelides", 
      genre: "Thriller",
      price: 19.99, 
      originalPrice: 26.99, 
      image: [
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=600&fit=crop",
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=600&fit=crop&flip=h"
      ], 
      rating: 4.6,
      description: "A psychological thriller about a woman who refuses to speak after allegedly murdering her husband.",
      color: "from-red-500 to-orange-500"
    },
    { 
      id: 5, 
      title: "The Midnight Library", 
      author: "Matt Haig", 
      genre: "Fiction",
      price: 21.99, 
      originalPrice: 29.99, 
      image: [
        "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop", 
        "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop&flip=h",
        "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop&flip=v"
      ], 
      rating: 4.5,
      description: "Between life and death there is a library, and within that library, the shelves go on forever. Every book provides a chance to try another life you could have lived.",
      color: "from-indigo-500 to-purple-500"
    },
    { 
      id: 6, 
      title: "Educated", 
      author: "Tara Westover", 
      genre: "Memoir",
      price: 20.99, 
      originalPrice: 27.99, 
      image: [
        "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=600&fit=crop",
        "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=600&fit=crop&flip=h"
      ], 
      rating: 4.7,
      description: "A memoir of family, resilience and self-invention. An unforgettable story about the transformative power of education.",
      color: "from-teal-500 to-cyan-500"
    },
  ];

  const newReleases = [
    { id: 1, title: "Fourth Wing", author: "Rebecca Ross", genre: "Fantasy", price: 26.99, image: ["https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=600&fit=crop", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=600&fit=crop&flip=h"], isNew: true, color: "from-purple-600 to-indigo-600" },
    { id: 2, title: "Tomorrow, and Tomorrow", author: "Gabrielle Zevin", genre: "Literary Fiction", price: 28.99, image: ["https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=600&fit=crop"], isNew: true, color: "from-blue-600 to-purple-600" },
    { id: 3, title: "The Atlas Six", author: "Olivie Blake", genre: "Dark Academia", price: 24.99, image: ["https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop", "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop&flip=v"], isNew: true, color: "from-indigo-600 to-purple-600" },
    { id: 4, title: "Project Hail Mary", author: "Andy Weir", genre: "Sci-Fi", price: 23.99, image: ["https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&h=600&fit=crop"], isNew: true, color: "from-cyan-600 to-blue-600" },
  ];

  const bookCategories = [
    { name: "Fiction", icon: "📚", color: "from-blue-500 to-indigo-600", books: "12,500+", description: "Imaginative stories and novels" },
    { name: "Non-Fiction", icon: "📖", color: "from-green-500 to-emerald-600", books: "8,200+", description: "Real stories and knowledge" },
    { name: "Mystery & Thriller", icon: "🔍", color: "from-purple-500 to-pink-600", books: "5,800+", description: "Suspense and intrigue" },
    { name: "Romance", icon: "💕", color: "from-pink-500 to-rose-600", books: "7,300+", description: "Love stories and passion" },
    { name: "Science Fiction", icon: "🚀", color: "from-cyan-500 to-blue-600", books: "4,600+", description: "Future worlds and technology" },
    { name: "Biography", icon: "👤", color: "from-orange-500 to-red-600", books: "3,900+", description: "Real lives and stories" },
  ];

  const heroSlides = [
    { 
      title: "Discover Your Next Great Read", 
      subtitle: "Explore thousands of books from bestselling authors and hidden gems", 
      cta: "Browse Collection", 
      bg: "bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700",
      icon: "🌟"
    },
    { 
      title: "New Releases & Bestsellers", 
      subtitle: "Stay updated with the latest books and trending titles", 
      cta: "See What's New", 
      bg: "bg-gradient-to-br from-purple-600 via-pink-600 to-rose-700",
      icon: "✨"
    },
    { 
      title: "Free Shipping on Orders Over $35", 
      subtitle: "Build your personal library with our extensive collection", 
      cta: "Start Shopping", 
      bg: "bg-gradient-to-br from-green-600 via-emerald-600 to-teal-700",
      icon: "🚚"
    },
  ];

  const BookCard = ({ book }: { book: any }) => (
    <div className="group relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 p-6 border border-gray-100 overflow-hidden transform hover:scale-105">
      <div className="absolute inset-0 bg-gradient-to-br from-gray-50 to-white opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      <div className="relative">
        <div className="relative mb-6">
          <div className="relative">
            <img 
              src={getBookImage(book.image)} 
              alt={book.title}
              className="w-full h-64 object-cover rounded-xl shadow-lg group-hover:shadow-xl transition-all duration-300"
            />
            <button className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-500 transition-all duration-300 transform hover:scale-110 bg-white/80 backdrop-blur-sm rounded-full p-2">
              ♡
            </button>
          </div>
          {book.isNew && (
            <div className="absolute -top-2 -right-2 bg-gradient-to-r from-red-500 to-pink-500 text-white text-xs px-3 py-1 rounded-full font-bold animate-pulse">
              NEW
            </div>
          )}
          
          {/* Rating Badge */}
          <div className="absolute top-2 left-2 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg px-2 py-1 shadow-lg backdrop-blur-sm border border-yellow-300">
            <div className="flex items-center gap-1">
              <span className="text-white font-bold text-xs">{book.rating}</span>
              <svg className="w-3 h-3 text-white fill-current" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
          </div>
        </div>
        <div className="text-center">
          <span className={`px-3 py-1 rounded-full text-xs font-bold mb-3 inline-block bg-gradient-to-r ${book.color} text-white shadow-md`}>
            {book.genre}
          </span>
          <h3 className="font-bold text-xl mb-2 text-gray-900 line-clamp-2 group-hover:text-blue-600 transition-colors duration-300">{book.title}</h3>
          <p className="text-gray-600 text-sm mb-4 font-medium">by {book.author}</p>
          <div className="flex items-center justify-center gap-2 mb-6">
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">${book.price}</span>
          </div>
          <div className="flex gap-3">
            <button className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 rounded-xl font-bold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105">
              Add to Cart
            </button>
            <button className="px-4 py-3 border-2 border-gray-300 hover:border-red-400 text-gray-700 hover:text-red-500 rounded-xl font-bold transition-all duration-300 hover:bg-red-50 transform hover:scale-105">
              ♡
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  // Featured Book Card - Horizontal Layout
  const FeaturedBookCard = ({ book }: { book: any }) => (
    <div className="group relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 p-6 border border-gray-100 overflow-hidden transform hover:scale-105">
      <div className="absolute inset-0 bg-gradient-to-br from-gray-50 to-white opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      <div className="relative flex gap-6">
        {/* Image Section - Left */}
        <div className="relative flex-shrink-0">
          <div className="relative">
            <img 
              src={getBookImage(book.image)} 
              alt={book.title}
              className="w-32 h-48 object-cover rounded-xl shadow-lg group-hover:shadow-xl transition-all duration-300"
            />
            <button className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-500 transition-all duration-300 transform hover:scale-110 bg-white/80 backdrop-blur-sm rounded-full p-1">
              ♡
            </button>
          </div>
          
          {/* Rating Badge */}
          <div className="absolute top-2 left-2 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg px-2 py-1 shadow-lg backdrop-blur-sm border border-yellow-300">
            <div className="flex items-center gap-1">
              <span className="text-white font-bold text-xs">{book.rating}</span>
              <svg className="w-3 h-3 text-white fill-current" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
          </div>
        </div>
        
        {/* Details Section - Right */}
        <div className="flex-1 flex flex-col justify-between">
          <div>
            <span className={`px-3 py-1 rounded-full text-xs font-bold mb-3 inline-block bg-gradient-to-r ${book.color} text-white shadow-md`}>
              {book.genre}
            </span>
            <h3 className="font-bold text-xl mb-2 text-gray-900 line-clamp-2 group-hover:text-blue-600 transition-colors duration-300">{book.title}</h3>
            <p className="text-gray-600 text-sm mb-3 font-medium">by {book.author}</p>
            <p className="text-gray-700 text-sm mb-4 line-clamp-3">{book.description}</p>
          </div>
          
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">${book.price}</span>
              {book.originalPrice && (
                <span className="text-sm text-gray-400 line-through">${book.originalPrice}</span>
              )}
            </div>
            <div className="flex gap-3">
              <button className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 rounded-xl font-bold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 text-sm">
                Add to Cart
              </button>
              <button className="px-4 py-3 border-2 border-gray-300 hover:border-red-400 text-gray-700 hover:text-red-500 rounded-xl font-bold transition-all duration-300 hover:bg-red-50 transform hover:scale-105">
                ♡
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const handleDropdownToggle = (menuKey: string) => {
    setActiveDropdown(activeDropdown === menuKey ? null : menuKey);
  };

  const handleDropdownClose = () => {
    setActiveDropdown(null);
  };

  const handleMobileMenuToggle = () => {
    setMobileMenuOpen(!mobileMenuOpen);
    setMobileDropdownOpen(null);
  };

  const handleMobileDropdownToggle = (menuKey: string) => {
    setMobileDropdownOpen(mobileDropdownOpen === menuKey ? null : menuKey);
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Element;
      if (!target.closest('.dropdown-menu')) {
        setActiveDropdown(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-lg sticky top-0 z-50 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
          <div className="flex items-center justify-between h-24 gap-8">
            {/* Logo */}
            <div className="flex-shrink-0">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent hover:scale-105 transition-transform duration-300">
                📚 BookHaven
              </h1>
            </div>
            
            {/* Right Actions */}
            <div className="flex items-center space-x-8">
              {/* Navigation Menu */}
              <nav className="hidden lg:flex items-center space-x-8">
                <button 
                  onClick={() => scrollToSection(heroRef)}
                  className="text-gray-700 hover:text-blue-600 transition-all duration-300 transform hover:scale-110 p-2 rounded-lg hover:bg-blue-50"
                >
                  <div className="flex flex-col items-center">
                    <span className="text-3xl mb-1">🏠</span>
                    <span className="text-xs font-semibold">Home</span>
                  </div>
                </button>
                
                {/* Dropdown Menus */}
                {Object.entries(dropdownMenus).map(([key, menu]) => (
                  <div key={key} className="relative group dropdown-menu">
                    <button
                      onClick={() => handleDropdownToggle(key)}
                      onMouseEnter={() => setActiveDropdown(key)}
                      className="text-gray-700 hover:text-blue-600 transition-all duration-300 transform hover:scale-110 p-2 rounded-lg hover:bg-blue-50"
                    >
                      <div className="flex flex-col items-center">
                        <span className="text-3xl mb-1">📋</span>
                        <div className="flex items-center gap-1">
                          <span className="text-xs font-semibold">{menu.title}</span>
                          <svg 
                            className={`w-3 h-3 transition-transform duration-300 ${activeDropdown === key ? 'rotate-180' : ''}`} 
                            fill="none" 
                            stroke="currentColor" 
                            viewBox="0 0 24 24"
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                          </svg>
                        </div>
                      </div>
                    </button>
                    
                    {/* Dropdown Content */}
                    <div 
                      className={`absolute top-full left-0 mt-8 w-[800px] bg-white rounded-xl shadow-2xl border border-gray-100 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 transform origin-top scale-95 group-hover:scale-100 z-50 ${activeDropdown === key ? 'opacity-100 visible scale-100' : ''}`}
                      onMouseLeave={() => setActiveDropdown(null)}
                    >
                      <div className="p-8">
                        <div className="text-xl font-bold text-gray-800 mb-6 text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                          Explore Our Collection
                        </div>
                        <div className="grid grid-cols-4 gap-6">
                          {menu.items.map((item, index) => (
                            <div key={index} className="relative group/item">
                              <button
                                onClick={item.action}
                                className="w-full text-center p-6 rounded-xl hover:bg-gradient-to-b hover:from-blue-50 hover:to-purple-50 transition-all duration-300 group-hover/item:shadow-lg border border-transparent hover:border-blue-200"
                              >
                                <div className="flex flex-col items-center space-y-4">
                                  <div className="text-5xl group-hover/item:scale-110 transition-transform duration-300">
                                    {item.icon}
                                  </div>
                                  <div>
                                    <div className="font-bold text-gray-800 group-hover/item:text-blue-600 transition-colors duration-300 text-xl">
                                      {item.name}
                                    </div>
                                    <div className="text-sm text-gray-500 mt-2">
                                      {item.description}
                                    </div>
                                  </div>
                                  <div className="w-12 h-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full opacity-0 group-hover/item:opacity-100 transition-opacity duration-300"></div>
                                </div>
                              </button>
                              
                              {/* Sub-menu on hover */}
                              <div className="absolute top-full left-0 mt-8 w-72 bg-white rounded-lg shadow-xl border border-gray-100 opacity-0 invisible group-hover/item:opacity-100 group-hover/item:visible transition-all duration-300 transform origin-top scale-95 group-hover/item:scale-100 z-50">
                                <div className="p-5">
                                  <div className="text-sm font-semibold text-gray-700 mb-4 px-4 py-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-md border-l-4 border-blue-500">
                                    {item.name}
                                  </div>
                                  {/* Desktop: Horizontal Grid Layout */}
                                  <div className="hidden lg:grid lg:grid-cols-2 gap-3">
                                    {item.subItems.map((subItem, subIndex) => (
                                      <button
                                        key={subIndex}
                                        onClick={subItem.action}
                                        className="w-full text-left px-4 py-3 text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-all duration-200 flex items-center justify-between group/sub hover:shadow-sm"
                                      >
                                        <span className="truncate">{subItem.name}</span>
                                        <svg 
                                          className="w-3 h-3 opacity-0 group-hover/sub:opacity-100 transition-opacity duration-200 flex-shrink-0" 
                                          fill="none" 
                                          stroke="currentColor" 
                                          viewBox="0 0 24 24"
                                        >
                                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                        </svg>
                                      </button>
                                    ))}
                                  </div>
                                  {/* Mobile: Vertical Layout (for smaller desktop screens) */}
                                  <div className="lg:hidden space-y-2">
                                    {item.subItems.map((subItem, subIndex) => (
                                      <button
                                        key={subIndex}
                                        onClick={subItem.action}
                                        className="w-full text-left px-4 py-3 text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-all duration-200 flex items-center justify-between group/sub hover:shadow-sm"
                                      >
                                        <span>{subItem.name}</span>
                                        <svg 
                                          className="w-3 h-3 opacity-0 group-hover/sub:opacity-100 transition-opacity duration-200 flex-shrink-0" 
                                          fill="none" 
                                          stroke="currentColor" 
                                          viewBox="0 0 24 24"
                                        >
                                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                        </svg>
                                      </button>
                                    ))}
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </nav>

              <button className="text-gray-700 hover:text-blue-600 transition-all duration-300 transform hover:scale-110 p-2 rounded-lg hover:bg-blue-50">
                <div className="flex flex-col items-center">
                  <span className="text-3xl mb-1">📖</span>
                  <span className="text-xs font-semibold">Wishlist</span>
                </div>
              </button>
              <button className="text-gray-700 hover:text-blue-600 transition-all duration-300 transform hover:scale-110 relative p-2 rounded-lg hover:bg-blue-50">
                <div className="flex flex-col items-center">
                  <span className="text-3xl mb-1">🛒</span>
                  <span className="text-xs font-semibold">Cart</span>
                  <span className="absolute -top-1 -right-1 bg-gradient-to-r from-red-500 to-pink-500 text-white text-xs rounded-full w-7 h-7 flex items-center justify-center font-bold">3</span>
                </div>
              </button>
              <button className="text-gray-700 hover:text-blue-600 font-semibold transition-colors duration-300 px-6 py-3 rounded-xl hover:bg-blue-50">
                Sign In
              </button>
              <button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-10 py-4 rounded-xl font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 text-lg">
                Join Now
              </button>
              
              {/* Mobile Menu Button */}
              <button
                onClick={handleMobileMenuToggle}
                className="lg:hidden text-gray-700 hover:text-blue-600 transition-colors duration-300 p-2 rounded-lg hover:bg-blue-50"
              >
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  {mobileMenuOpen ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  ) : (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  )}
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-white border-b border-gray-200 shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <nav className="space-y-2">
              <button 
                onClick={() => {
                  scrollToSection(heroRef);
                  setMobileMenuOpen(false);
                }}
                className="w-full text-left px-4 py-3 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200 font-medium flex items-center gap-3"
              >
                <span className="text-xl">🏠</span>
                Home
              </button>
              
              {Object.entries(dropdownMenus).map(([key, menu]) => (
                <div key={key} className="space-y-1">
                  <button
                    onClick={() => handleMobileDropdownToggle(key)}
                    className="w-full text-left px-4 py-3 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200 font-medium flex items-center justify-between"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-xl">📋</span>
                      <span>{menu.title}</span>
                    </div>
                    <svg 
                      className={`w-4 h-4 transition-transform duration-300 ${mobileDropdownOpen === key ? 'rotate-180' : ''}`} 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  
                  {mobileDropdownOpen === key && (
                    <div className="ml-4 space-y-4 bg-gray-50 rounded-lg p-4 border border-gray-200 shadow-sm">
                      <div className="text-sm font-bold text-gray-700 text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                        Explore Our Collection
                      </div>
                      <div className="grid grid-cols-2 gap-3">
                        {menu.items.map((item, index) => (
                          <div key={index} className="space-y-2">
                            <button
                              onClick={() => {
                                item.action();
                                setMobileMenuOpen(false);
                                setMobileDropdownOpen(null);
                              }}
                              className="w-full text-center px-4 py-4 text-gray-600 hover:text-blue-600 hover:bg-blue-100 rounded-lg transition-all duration-200 flex flex-col items-center space-y-2 border border-gray-200 hover:border-blue-300"
                            >
                              <span className="text-3xl">{item.icon}</span>
                              <div>
                                <div className="font-bold text-sm">{item.name}</div>
                                <div className="text-xs text-gray-500">{item.description}</div>
                              </div>
                            </button>
                            
                            {/* Mobile sub-items - Vertical Layout */}
                            <div className="space-y-1 bg-white rounded-lg p-3 border border-gray-200 shadow-sm">
                              <div className="text-xs font-semibold text-gray-500 mb-2 px-2 py-1 bg-gray-100 rounded-md text-center">
                                {item.name} Options
                              </div>
                              <div className="space-y-1">
                                {item.subItems.map((subItem, subIndex) => (
                                  <button
                                    key={subIndex}
                                    onClick={() => {
                                      subItem.action();
                                      setMobileMenuOpen(false);
                                      setMobileDropdownOpen(null);
                                    }}
                                    className="w-full text-left px-3 py-2 text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-all duration-200 flex items-center justify-between group/sub"
                                  >
                                    <span>{subItem.name}</span>
                                    <svg 
                                      className="w-3 h-3 opacity-0 group-hover/sub:opacity-100 transition-opacity duration-200" 
                                      fill="none" 
                                      stroke="currentColor" 
                                      viewBox="0 0 24 24"
                                    >
                                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                    </svg>
                                  </button>
                                ))}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </nav>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Search Section */}
        <section className="py-16 bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 rounded-3xl my-8">
          <div className="text-center mb-12">
            <h2 className="text-5xl font-bold text-gray-900 mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Find Your Next Favorite Book
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Discover millions of books across all genres. Search by title, author, ISBN, or explore our curated collections.
            </p>
          </div>
          
          <div className="max-w-4xl mx-auto">
            <div className="relative">
              <input
                type="text"
                placeholder="Search books, authors, ISBN, or browse categories..."
                className="w-full px-8 py-6 pl-20 pr-8 text-gray-700 bg-white border-2 border-gray-200 rounded-3xl focus:outline-none focus:border-blue-500 focus:ring-8 focus:ring-blue-200/30 transition-all duration-300 text-xl shadow-lg hover:shadow-xl"
              />
              <div className="absolute inset-y-0 left-0 flex items-center pl-8">
                <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <button className="absolute inset-y-0 right-0 flex items-center pr-6">
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-3 rounded-2xl font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105">
                  Search
                </div>
              </button>
            </div>
            
            {/* Quick Search Categories */}
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              <button className="px-6 py-3 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-2xl text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105">
                📚 Fiction
              </button>
              <button className="px-6 py-3 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-2xl text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105">
                🔬 Science Fiction
              </button>
              <button className="px-6 py-3 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-2xl text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105">
                💕 Romance
              </button>
              <button className="px-6 py-3 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-2xl text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105">
                🕵️ Mystery
              </button>
              <button className="px-6 py-3 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-2xl text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105">
                📖 Non-Fiction
              </button>
              <button className="px-6 py-3 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-2xl text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105">
                🎯 Bestsellers
              </button>
            </div>
          </div>
        </section>

        {/* Hero Section */}
        <section ref={heroRef} className="py-20">
          <div className={`relative h-[500px] rounded-3xl overflow-hidden mb-16 shadow-2xl ${isVisible ? 'animate-fade-in' : ''}`}>
            <div className={`absolute inset-0 ${heroSlides[currentSlide].bg} flex items-center justify-center text-white`}>
              <div className="text-center max-w-5xl px-8">
                <div className="text-8xl mb-6 animate-bounce">{heroSlides[currentSlide].icon}</div>
                <h2 className="text-6xl font-bold mb-8 leading-tight drop-shadow-lg">{heroSlides[currentSlide].title}</h2>
                <p className="text-2xl mb-10 opacity-90 leading-relaxed">{heroSlides[currentSlide].subtitle}</p>
                <button className="bg-white text-gray-800 px-10 py-5 rounded-2xl font-bold hover:bg-gray-100 transition-all duration-300 shadow-2xl hover:shadow-3xl transform hover:scale-105 text-lg">
                  {heroSlides[currentSlide].cta}
                </button>
              </div>
            </div>
            
            {/* Slide Indicators */}
            <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-4">
              {heroSlides.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentSlide(index)}
                  className={`w-4 h-4 rounded-full transition-all duration-300 ${
                    index === currentSlide ? 'bg-white scale-125 shadow-lg' : 'bg-white/50 hover:bg-white/75'
                  }`}
                />
              ))}
            </div>
          </div>
        </section>

        {/* Featured Books Slider */}
        <section ref={featuredRef} className="py-20">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold text-gray-900 mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Featured Books
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Handpicked selections from our curators - discover your next favorite read
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {featuredBooks.map((book) => (
              <FeaturedBookCard key={book.id} book={book} />
            ))}
          </div>
        </section>

        {/* New Releases */}
        <section ref={newReleasesRef} className="py-20 bg-gradient-to-br from-gray-50 to-white -mx-4 sm:-mx-6 lg:-mx-8 px-4 sm:px-6 lg:px-8 rounded-3xl">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold text-gray-900 mb-6 bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
              New Releases
            </h2>
            <p className="text-xl text-gray-600">Fresh off the press - the latest books everyone's talking about</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {newReleases.map((book) => (
              <BookCard key={book.id} book={book} />
            ))}
          </div>
        </section>

        {/* Browse by Category */}
        <section ref={categoriesRef} className="py-20">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold text-gray-900 mb-6 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Browse by Genre
            </h2>
            <p className="text-xl text-gray-600">Explore our extensive collection across all your favorite genres</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {bookCategories.map((category, index) => (
              <div
                key={index}
                className={`relative overflow-hidden rounded-3xl p-8 text-center cursor-pointer transition-all duration-500 hover:scale-105 hover:shadow-2xl group bg-gradient-to-br ${category.color} text-white`}
              >
                <div className="absolute inset-0 bg-black/10 group-hover:bg-black/20 transition-all duration-300"></div>
                <div className="relative">
                  <div className="text-7xl mb-6 group-hover:scale-110 transition-transform duration-300">{category.icon}</div>
                  <h3 className="font-bold text-2xl mb-3">{category.name}</h3>
                  <p className="text-lg mb-4 opacity-90">{category.description}</p>
                  <p className="text-2xl font-bold">{category.books} books</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Why Choose Us */}
        <section ref={whyChooseRef} className="py-20 bg-gradient-to-br from-blue-50 to-purple-50 -mx-4 sm:-mx-6 lg:-mx-8 px-4 sm:px-6 lg:px-8 rounded-3xl">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold text-gray-900 mb-6 bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
              Why BookHaven?
            </h2>
            <p className="text-xl text-gray-600">More than just a bookstore - we're your reading companion</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="text-center group">
              <div className="text-8xl mb-6 group-hover:scale-110 transition-transform duration-300">🚚</div>
              <h3 className="text-2xl font-bold mb-4 text-gray-900">Free Shipping</h3>
              <p className="text-gray-600 leading-relaxed">Free delivery on orders over $35. Fast, secure, and reliable shipping worldwide.</p>
            </div>
            <div className="text-center group">
              <div className="text-8xl mb-6 group-hover:scale-110 transition-transform duration-300">💯</div>
              <h3 className="text-2xl font-bold mb-4 text-gray-900">Satisfaction Guarantee</h3>
              <p className="text-gray-600 leading-relaxed">30-day return policy. Not happy with your purchase? Return it hassle-free.</p>
            </div>
            <div className="text-center group">
              <div className="text-8xl mb-6 group-hover:scale-110 transition-transform duration-300">🎯</div>
              <h3 className="text-2xl font-bold mb-4 text-gray-900">Personalized Recommendations</h3>
              <p className="text-gray-600 leading-relaxed">AI-powered suggestions based on your reading history and preferences.</p>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section ref={ctaRef} className="py-20 text-center">
          <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 rounded-3xl p-16 text-white shadow-2xl">
            <h2 className="text-5xl font-bold mb-6">Join Our Reading Community</h2>
            <p className="text-2xl mb-10 opacity-90 leading-relaxed">
              Get exclusive access to new releases, author events, and personalized book recommendations
            </p>
            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <button className="bg-white text-blue-600 px-10 py-5 rounded-2xl font-bold hover:bg-gray-100 transition-all duration-300 shadow-2xl hover:shadow-3xl transform hover:scale-105 text-lg">
                Sign Up Free
              </button>
              <button className="border-3 border-white text-white px-10 py-5 rounded-2xl font-bold hover:bg-white hover:text-blue-600 transition-all duration-300 shadow-2xl hover:shadow-3xl transform hover:scale-105 text-lg">
                Browse Catalog
              </button>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white py-16 -mx-4 sm:-mx-6 lg:-mx-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
            <div>
              <h3 className="text-2xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                📚 BookHaven
              </h3>
              <p className="text-gray-400 leading-relaxed text-lg">
                Your premier destination for books, connecting readers with stories that inspire, educate, and entertain.
              </p>
            </div>
            <div>
              <h4 className="font-bold text-xl mb-6">Shop</h4>
              <ul className="space-y-3 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors duration-300 text-lg">New Releases</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-300 text-lg">Bestsellers</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-300 text-lg">Fiction</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-300 text-lg">Non-Fiction</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-xl mb-6">Support</h4>
              <ul className="space-y-3 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors duration-300 text-lg">Help Center</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-300 text-lg">Shipping Info</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-300 text-lg">Returns</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-300 text-lg">Contact Us</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-xl mb-6">Connect</h4>
              <div className="flex space-x-6 mb-6">
                <a href="#" className="text-gray-400 hover:text-white transition-colors duration-300 text-2xl transform hover:scale-110">📘</a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors duration-300 text-2xl transform hover:scale-110">📷</a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors duration-300 text-2xl transform hover:scale-110">🐦</a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors duration-300 text-2xl transform hover:scale-110">📧</a>
              </div>
              <p className="text-gray-400 text-lg">Follow us for book recommendations and literary news</p>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p className="text-lg">&copy; 2024 BookHaven. All rights reserved. | Privacy Policy | Terms of Service</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;