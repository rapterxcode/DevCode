import React from 'react';
import { searchData } from '../data';

const SearchSection: React.FC = () => {
  return (
    <section className="py-16 bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 rounded-3xl my-8">
      <div className="text-center mb-12">
        <h2 className="text-5xl font-bold text-gray-900 mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          {searchData.title}
        </h2>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
          {searchData.subtitle}
        </p>
      </div>
      
      <div className="max-w-4xl mx-auto">
        <div className="relative">
          <input
            type="text"
            placeholder={searchData.placeholder}
            className="w-full px-8 py-6 pl-20 pr-8 text-gray-700 bg-white border-2 border-gray-200 rounded-3xl focus:outline-none focus:border-blue-500 focus:ring-8 focus:ring-blue-200/30 transition-all duration-300 text-xl shadow-lg hover:shadow-xl"
          />
          <div className="absolute inset-y-0 left-0 flex items-center pl-8">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <button className="absolute inset-y-0 right-0 flex items-center pr-6">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-3 rounded-2xl font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105">
              {searchData.searchButtonText}
            </div>
          </button>
        </div>
        
        {/* Quick Search Categories */}
        <div className="mt-8 flex flex-wrap justify-center gap-4">
          {searchData.quickSearchCategories.map((category) => (
            <button 
              key={category.id}
              className="px-6 py-3 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-2xl text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105"
              title={category.description}
            >
              {category.icon} {category.name}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
};

export default SearchSection; 