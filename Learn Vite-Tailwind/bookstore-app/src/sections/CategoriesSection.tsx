import React from 'react';
import type { BookCategory } from '../data';

interface CategoriesSectionProps {
  categoriesRef: React.RefObject<HTMLDivElement | null>;
  bookCategories: BookCategory[];
}

const CategoriesSection: React.FC<CategoriesSectionProps> = ({
  categoriesRef,
  bookCategories
}) => {
  return (
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
  );
};

export default CategoriesSection; 