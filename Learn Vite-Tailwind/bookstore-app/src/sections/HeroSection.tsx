import React from 'react';
import type { HeroSlide } from '../data';

interface HeroSectionProps {
  heroRef: React.RefObject<HTMLDivElement | null>;
  currentSlide: number;
  isVisible: boolean;
  heroSlides: HeroSlide[];
  setCurrentSlide: (slide: number) => void;
}

const HeroSection: React.FC<HeroSectionProps> = ({
  heroRef,
  currentSlide,
  isVisible,
  heroSlides,
  setCurrentSlide
}) => {
  return (
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
  );
};

export default HeroSection; 