import React from 'react';
import { whyChooseData } from '../data';

interface WhyChooseSectionProps {
  whyChooseRef: React.RefObject<HTMLDivElement | null>;
}

const WhyChooseSection: React.FC<WhyChooseSectionProps> = ({ whyChooseRef }) => {
  return (
    <section ref={whyChooseRef} className="py-20 bg-gradient-to-br from-blue-50 to-purple-50 -mx-4 sm:-mx-6 lg:-mx-8 px-4 sm:px-6 lg:px-8 rounded-3xl">
      <div className="text-center mb-16">
        <h2 className="text-5xl font-bold text-gray-900 mb-6 bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
          {whyChooseData.title}
        </h2>
        <p className="text-xl text-gray-600">{whyChooseData.subtitle}</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
        {whyChooseData.features.map((feature) => (
          <div key={feature.id} className="text-center group">
            <div className="text-8xl mb-6 group-hover:scale-110 transition-transform duration-300">
              {feature.icon}
            </div>
            <h3 className="text-2xl font-bold mb-4 text-gray-900">{feature.title}</h3>
            <p className="text-gray-600 leading-relaxed">{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default WhyChooseSection; 