import React from 'react';
import type { Book } from '../data';

interface FeaturedBookCardProps {
  book: Book;
}

const FeaturedBookCard: React.FC<FeaturedBookCardProps> = ({ book }) => {
  // Helper function to get image from array
  const getBookImage = (imageArray: string[], index: number = 0) => {
    return imageArray[index] || imageArray[0] || '/default-book-cover.jpg';
  };

  return (
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
};

export default FeaturedBookCard; 