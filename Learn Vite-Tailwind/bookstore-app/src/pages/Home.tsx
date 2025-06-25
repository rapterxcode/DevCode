import React, { useState, useEffect, useRef } from 'react';
import { 
  createDropdownMenus, 
  featuredBooks, 
  newReleases, 
  bookCategories, 
  heroSlides 
} from '../data';
import { Header, Footer } from '../components';
import {
  SearchSection,
  HeroSection,
  FeaturedBooksSection,
  NewReleasesSection,
  CategoriesSection,
  WhyChooseSection,
  CTASection
} from '../sections';

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

  // Smooth scroll function
  const scrollToSection = (ref: React.RefObject<HTMLDivElement | null>) => {
    ref.current?.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
    setActiveDropdown(null); // Close dropdown after navigation
  };

  // Create dropdown menus with scroll functions
  const dropdownMenus = createDropdownMenus(
    scrollToSection,
    featuredRef,
    newReleasesRef,
    categoriesRef,
    whyChooseRef,
    ctaRef
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
        0%, 25% { opacity:1; }
        33%, 100% { opacity:0; }
      }
      @keyframes pulse {
        0%, 25% { opacity:1; transform: scale(1.25); }
        33%, 100% { opacity:0.5; transform: scale(1); }
      }
    `;
    document.head.appendChild(style);
    return () => {
      document.head.removeChild(style);
    };
  }, []);

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
      <Header
        dropdownMenus={dropdownMenus}
        activeDropdown={activeDropdown}
        mobileMenuOpen={mobileMenuOpen}
        mobileDropdownOpen={mobileDropdownOpen}
        onDropdownToggle={handleDropdownToggle}
        onDropdownClose={handleDropdownClose}
        onMobileMenuToggle={handleMobileMenuToggle}
        onMobileDropdownToggle={handleMobileDropdownToggle}
        scrollToSection={scrollToSection}
        heroRef={heroRef}
      />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Search Section */}
        <SearchSection />

        {/* Hero Section */}
        <HeroSection
          heroRef={heroRef}
          currentSlide={currentSlide}
          isVisible={isVisible}
          heroSlides={heroSlides}
          setCurrentSlide={setCurrentSlide}
        />

        {/* Featured Books Section */}
        <FeaturedBooksSection
          featuredRef={featuredRef}
          featuredBooks={featuredBooks}
        />

        {/* New Releases Section */}
        <NewReleasesSection
          newReleasesRef={newReleasesRef}
          newReleases={newReleases}
        />

        {/* Categories Section */}
        <CategoriesSection
          categoriesRef={categoriesRef}
          bookCategories={bookCategories}
        />

        {/* Why Choose Us Section */}
        <WhyChooseSection whyChooseRef={whyChooseRef} />

        {/* CTA Section */}
        <CTASection ctaRef={ctaRef} />
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Home;