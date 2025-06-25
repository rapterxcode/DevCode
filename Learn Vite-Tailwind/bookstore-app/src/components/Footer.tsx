import React from 'react';
import { footerData } from '../data';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white py-16 -mx-4 sm:-mx-6 lg:-mx-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          <div>
            <h3 className="text-2xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              {footerData.brand.icon} {footerData.brand.name}
            </h3>
            <p className="text-gray-400 leading-relaxed text-lg">
              {footerData.brand.description}
            </p>
          </div>
          
          {footerData.sections.map((section) => (
            <div key={section.id}>
              <h4 className="font-bold text-xl mb-6">{section.title}</h4>
              <ul className="space-y-3 text-gray-400">
                {section.links.map((link) => (
                  <li key={link.id}>
                    <a 
                      href={link.url} 
                      className="hover:text-white transition-colors duration-300 text-lg"
                    >
                      {link.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
          
          <div>
            <h4 className="font-bold text-xl mb-6">Connect</h4>
            <div className="flex space-x-6 mb-6">
              {footerData.socialLinks.map((socialLink) => (
                <a 
                  key={socialLink.id}
                  href={socialLink.url} 
                  className="text-gray-400 hover:text-white transition-colors duration-300 text-2xl transform hover:scale-110"
                  title={socialLink.name}
                >
                  {socialLink.icon}
                </a>
              ))}
            </div>
            <p className="text-gray-400 text-lg">{footerData.socialDescription}</p>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
          <p className="text-lg">{footerData.copyright}</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 