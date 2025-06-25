import React from 'react';
import BookCard from '../components/BookCard';
import type { Book } from '../data';

interface NewReleasesSectionProps {
  newReleasesRef: React.RefObject<HTMLDivElement | null>;
  newReleases: Book[];
}

const NewReleasesSection: React.FC<NewReleasesSectionProps> = ({
  newReleasesRef,
  newReleases
}) => {
  return (
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
  );
};

export default NewReleasesSection; 