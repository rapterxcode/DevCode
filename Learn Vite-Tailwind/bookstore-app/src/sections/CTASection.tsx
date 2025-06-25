import React from 'react';

interface CTASectionProps {
  ctaRef: React.RefObject<HTMLDivElement | null>;
}

const CTASection: React.FC<CTASectionProps> = ({ ctaRef }) => {
  return (
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
  );
};

export default CTASection; 