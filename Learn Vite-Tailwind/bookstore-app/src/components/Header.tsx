import React from 'react';
import type { DropdownMenus } from '../data';
import { headerData } from '../data';

interface HeaderProps {
  dropdownMenus: DropdownMenus;
  activeDropdown: string | null;
  mobileMenuOpen: boolean;
  mobileDropdownOpen: string | null;
  onDropdownToggle: (menuKey: string) => void;
  onDropdownClose: () => void;
  onMobileMenuToggle: () => void;
  onMobileDropdownToggle: (menuKey: string) => void;
  scrollToSection: (ref: React.RefObject<HTMLDivElement | null>) => void;
  heroRef: React.RefObject<HTMLDivElement | null>;
}

const Header: React.FC<HeaderProps> = ({
  dropdownMenus,
  activeDropdown,
  mobileMenuOpen,
  mobileDropdownOpen,
  onDropdownToggle,
  onDropdownClose,
  onMobileMenuToggle,
  onMobileDropdownToggle,
  scrollToSection,
  heroRef
}) => {
  return (
    <>
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-lg sticky top-0 z-50 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
          <div className="flex items-center justify-between h-24 gap-8">
            {/* Logo */}
            <div className="flex-shrink-0">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent hover:scale-105 transition-transform duration-300">
                {headerData.brand.icon} {headerData.brand.name}
              </h1>
            </div>
            
            {/* Right Actions */}
            <div className="flex items-center space-x-8">
              {/* Navigation Menu */}
              <nav className="hidden lg:flex items-center space-x-8">
                {/* Navigation Buttons */}
                {headerData.navigationButtons.map((button) => (
                  <button 
                    key={button.id}
                    onClick={() => scrollToSection(heroRef)}
                    className="text-gray-700 hover:text-blue-600 transition-all duration-300 transform hover:scale-110 p-2 rounded-lg hover:bg-blue-50"
                  >
                    <div className="flex flex-col items-center">
                      <span className="text-3xl mb-1">{button.icon}</span>
                      <span className="text-xs font-semibold">{button.label}</span>
                    </div>
                  </button>
                ))}
                
                {/* Dropdown Menus */}
                {Object.entries(dropdownMenus).map(([key, menu]) => (
                  <div key={key} className="relative group dropdown-menu">
                    <button
                      onClick={() => onDropdownToggle(key)}
                      onMouseEnter={() => onDropdownToggle(key)}
                      className="text-gray-700 hover:text-blue-600 transition-all duration-300 transform hover:scale-110 p-2 rounded-lg hover:bg-blue-50"
                    >
                      <div className="flex flex-col items-center">
                        <span className="text-3xl mb-1">📋</span>
                        <div className="flex items-center gap-1">
                          <span className="text-xs font-semibold">{menu.title}</span>
                          <svg 
                            className={`w-3 h-3 transition-transform duration-300 ${activeDropdown === key ? 'rotate-180' : ''}`} 
                            fill="none" 
                            stroke="currentColor" 
                            viewBox="0 0 24 24"
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                          </svg>
                        </div>
                      </div>
                    </button>
                    
                    {/* Dropdown Content */}
                    <div 
                      className={`absolute top-full left-0 mt-8 w-[800px] bg-white rounded-xl shadow-2xl border border-gray-100 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 transform origin-top scale-95 group-hover:scale-100 z-50 ${activeDropdown === key ? 'opacity-100 visible scale-100' : ''}`}
                      onMouseLeave={onDropdownClose}
                    >
                      <div className="p-8">
                        <div className="text-xl font-bold text-gray-800 mb-6 text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                          Explore Our Collection
                        </div>
                        <div className="grid grid-cols-4 gap-6">
                          {menu.items.map((item, index) => (
                            <div key={index} className="relative group/item">
                              <button
                                onClick={item.action}
                                className="w-full text-center p-6 rounded-xl hover:bg-gradient-to-b hover:from-blue-50 hover:to-purple-50 transition-all duration-300 group-hover/item:shadow-lg border border-transparent hover:border-blue-200"
                              >
                                <div className="flex flex-col items-center space-y-4">
                                  <div className="text-5xl group-hover/item:scale-110 transition-transform duration-300">
                                    {item.icon}
                                  </div>
                                  <div>
                                    <div className="font-bold text-gray-800 group-hover/item:text-blue-600 transition-colors duration-300 text-xl">
                                      {item.name}
                                    </div>
                                    <div className="text-sm text-gray-500 mt-2">
                                      {item.description}
                                    </div>
                                  </div>
                                  <div className="w-12 h-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full opacity-0 group-hover/item:opacity-100 transition-opacity duration-300"></div>
                                </div>
                              </button>
                              
                              {/* Sub-menu on hover */}
                              <div className="absolute top-full left-0 mt-8 w-72 bg-white rounded-lg shadow-xl border border-gray-100 opacity-0 invisible group-hover/item:opacity-100 group-hover/item:visible transition-all duration-300 transform origin-top scale-95 group-hover/item:scale-100 z-50">
                                <div className="p-5">
                                  <div className="text-sm font-semibold text-gray-700 mb-4 px-4 py-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-md border-l-4 border-blue-500">
                                    {item.name}
                                  </div>
                                  {/* Desktop: Horizontal Grid Layout */}
                                  <div className="hidden lg:grid lg:grid-cols-2 gap-3">
                                    {item.subItems.map((subItem, subIndex) => (
                                      <button
                                        key={subIndex}
                                        onClick={subItem.action}
                                        className="w-full text-left px-4 py-3 text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-all duration-200 flex items-center justify-between group/sub hover:shadow-sm"
                                      >
                                        <span className="truncate">{subItem.name}</span>
                                        <svg 
                                          className="w-3 h-3 opacity-0 group-hover/sub:opacity-100 transition-opacity duration-200 flex-shrink-0" 
                                          fill="none" 
                                          stroke="currentColor" 
                                          viewBox="0 0 24 24"
                                        >
                                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                        </svg>
                                      </button>
                                    ))}
                                  </div>
                                  {/* Mobile: Vertical Layout (for smaller desktop screens) */}
                                  <div className="lg:hidden space-y-2">
                                    {item.subItems.map((subItem, subIndex) => (
                                      <button
                                        key={subIndex}
                                        onClick={subItem.action}
                                        className="w-full text-left px-4 py-3 text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-all duration-200 flex items-center justify-between group/sub hover:shadow-sm"
                                      >
                                        <span>{subItem.name}</span>
                                        <svg 
                                          className="w-3 h-3 opacity-0 group-hover/sub:opacity-100 transition-opacity duration-200 flex-shrink-0" 
                                          fill="none" 
                                          stroke="currentColor" 
                                          viewBox="0 0 24 24"
                                        >
                                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                        </svg>
                                      </button>
                                    ))}
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}

                {/* Action Buttons */}
                {headerData.actionButtons.map((button) => (
                  <button 
                    key={button.id}
                    className="text-gray-700 hover:text-blue-600 transition-all duration-300 transform hover:scale-110 relative p-2 rounded-lg hover:bg-blue-50"
                  >
                    <div className="flex flex-col items-center">
                      <span className="text-3xl mb-1">{button.icon}</span>
                      <span className="text-xs font-semibold">{button.label}</span>
                      {button.badge && (
                        <span className="absolute -top-1 -right-1 bg-gradient-to-r from-red-500 to-pink-500 text-white text-xs rounded-full w-7 h-7 flex items-center justify-center font-bold">
                          {button.badge}
                        </span>
                      )}
                    </div>
                  </button>
                ))}

                {/* Auth Buttons */}
                {headerData.authButtons.map((button, index) => (
                  <button 
                    key={button.id}
                    className={`${
                      index === headerData.authButtons.length - 1 
                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-10 py-4 rounded-xl font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 text-lg'
                        : 'text-gray-700 hover:text-blue-600 font-semibold transition-colors duration-300 px-6 py-3 rounded-xl hover:bg-blue-50'
                    }`}
                  >
                    {button.label}
                  </button>
                ))}
              </nav>

              {/* Mobile Menu Button */}
              <button
                onClick={onMobileMenuToggle}
                className="lg:hidden text-gray-700 hover:text-blue-600 transition-colors duration-300 p-2 rounded-lg hover:bg-blue-50"
              >
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  {mobileMenuOpen ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  ) : (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  )}
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-white border-b border-gray-200 shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <nav className="space-y-2">
              {/* Mobile Navigation Buttons */}
              {headerData.navigationButtons.map((button) => (
                <button 
                  key={button.id}
                  onClick={() => {
                    scrollToSection(heroRef);
                    onMobileMenuToggle();
                  }}
                  className="w-full text-left px-4 py-3 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200 font-medium flex items-center gap-3"
                >
                  <span className="text-xl">{button.icon}</span>
                  {button.label}
                </button>
              ))}
              
              {/* Mobile Action Buttons */}
              {headerData.actionButtons.map((button) => (
                <button 
                  key={button.id}
                  className="w-full text-left px-4 py-3 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200 font-medium flex items-center gap-3"
                >
                  <span className="text-xl">{button.icon}</span>
                  {button.label}
                  {button.badge && (
                    <span className="ml-auto bg-gradient-to-r from-red-500 to-pink-500 text-white text-xs rounded-full px-2 py-1 font-bold">
                      {button.badge}
                    </span>
                  )}
                </button>
              ))}

              {/* Mobile Auth Buttons */}
              {headerData.authButtons.map((button, index) => (
                <button 
                  key={button.id}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-all duration-200 font-medium ${
                    index === headerData.authButtons.length - 1 
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                      : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
                  }`}
                >
                  {button.label}
                </button>
              ))}
              
              {/* Mobile Dropdown Menus */}
              {Object.entries(dropdownMenus).map(([key, menu]) => (
                <div key={key} className="space-y-1">
                  <button
                    onClick={() => onMobileDropdownToggle(key)}
                    className="w-full text-left px-4 py-3 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200 font-medium flex items-center justify-between"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-xl">📋</span>
                      <span>{menu.title}</span>
                    </div>
                    <svg 
                      className={`w-4 h-4 transition-transform duration-300 ${mobileDropdownOpen === key ? 'rotate-180' : ''}`} 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  
                  {mobileDropdownOpen === key && (
                    <div className="ml-4 space-y-4 bg-gray-50 rounded-lg p-4 border border-gray-200 shadow-sm">
                      <div className="text-sm font-bold text-gray-700 text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                        Explore Our Collection
                      </div>
                      <div className="grid grid-cols-2 gap-3">
                        {menu.items.map((item, index) => (
                          <div key={index} className="space-y-2">
                            <button
                              onClick={() => {
                                item.action();
                                onMobileMenuToggle();
                                onMobileDropdownToggle(key);
                              }}
                              className="w-full text-center px-4 py-4 text-gray-600 hover:text-blue-600 hover:bg-blue-100 rounded-lg transition-all duration-200 flex flex-col items-center space-y-2 border border-gray-200 hover:border-blue-300"
                            >
                              <span className="text-3xl">{item.icon}</span>
                              <div>
                                <div className="font-bold text-sm">{item.name}</div>
                                <div className="text-xs text-gray-500">{item.description}</div>
                              </div>
                            </button>
                            
                            {/* Mobile sub-items - Vertical Layout */}
                            <div className="space-y-1 bg-white rounded-lg p-3 border border-gray-200 shadow-sm">
                              <div className="text-xs font-semibold text-gray-500 mb-2 px-2 py-1 bg-gray-100 rounded-md text-center">
                                {item.name} Options
                              </div>
                              <div className="space-y-1">
                                {item.subItems.map((subItem, subIndex) => (
                                  <button
                                    key={subIndex}
                                    onClick={() => {
                                      subItem.action();
                                      onMobileMenuToggle();
                                      onMobileDropdownToggle(key);
                                    }}
                                    className="w-full text-left px-3 py-2 text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-all duration-200 flex items-center justify-between group/sub"
                                  >
                                    <span>{subItem.name}</span>
                                    <svg 
                                      className="w-3 h-3 opacity-0 group-hover/sub:opacity-100 transition-opacity duration-200" 
                                      fill="none" 
                                      stroke="currentColor" 
                                      viewBox="0 0 24 24"
                                    >
                                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                    </svg>
                                  </button>
                                ))}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </nav>
          </div>
        </div>
      )}
    </>
  );
};

export default Header; 