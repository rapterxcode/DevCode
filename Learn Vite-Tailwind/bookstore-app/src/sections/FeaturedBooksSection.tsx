import React from 'react';
import FeaturedBookCard from '../components/FeaturedBookCard';
import type { Book } from '../data';

interface FeaturedBooksSectionProps {
  featuredRef: React.RefObject<HTMLDivElement | null>;
  featuredBooks: Book[];
}

const FeaturedBooksSection: React.FC<FeaturedBooksSectionProps> = ({
  featuredRef,
  featuredBooks
}) => {
  return (
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
  );
};

export default FeaturedBooksSection; 