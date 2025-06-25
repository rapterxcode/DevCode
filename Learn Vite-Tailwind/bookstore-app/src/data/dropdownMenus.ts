export interface DropdownItem {
  name: string;
  description: string;
  icon: string;
  action: () => void;
  subItems: {
    name: string;
    action: () => void;
  }[];
}

export interface DropdownMenu {
  title: string;
  items: DropdownItem[];
}

export interface DropdownMenus {
  menu: DropdownMenu;
}

// This will be populated with actual scroll functions when imported
export const createDropdownMenus = (
  scrollToSection: (ref: React.RefObject<HTMLDivElement | null>) => void,
  featuredRef: React.RefObject<HTMLDivElement | null>,
  newReleasesRef: React.RefObject<HTMLDivElement | null>,
  categoriesRef: React.RefObject<HTMLDivElement | null>,
  whyChooseRef: React.RefObject<HTMLDivElement | null>,
  ctaRef: React.RefObject<HTMLDivElement | null>
): DropdownMenus => ({
  menu: {
    title: "Menu",
    items: [
      { 
        name: "Books", 
        description: "Explore our collection",
        icon: "📚",
        action: () => scrollToSection(featuredRef),
        subItems: [
          { name: "Featured Books", action: () => scrollToSection(featuredRef) },
          { name: "New Releases", action: () => scrollToSection(newReleasesRef) },
          { name: "Bestsellers", action: () => scrollToSection(featuredRef) },
          { name: "Coming Soon", action: () => scrollToSection(newReleasesRef) }
        ]
      },
      { 
        name: "Categories", 
        description: "Browse by genre",
        icon: "📖",
        action: () => scrollToSection(categoriesRef),
        subItems: [
          { name: "Fiction", action: () => scrollToSection(categoriesRef) },
          { name: "Non-Fiction", action: () => scrollToSection(categoriesRef) },
          { name: "Science Fiction", action: () => scrollToSection(categoriesRef) },
          { name: "Mystery & Thriller", action: () => scrollToSection(categoriesRef) },
          { name: "Romance", action: () => scrollToSection(categoriesRef) },
          { name: "Biography", action: () => scrollToSection(categoriesRef) }
        ]
      },
      { 
        name: "Services", 
        description: "Additional services",
        icon: "🎯",
        action: () => scrollToSection(whyChooseRef),
        subItems: [
          { name: "Book Clubs", action: () => scrollToSection(whyChooseRef) },
          { name: "Author Events", action: () => scrollToSection(whyChooseRef) },
          { name: "Reading Lists", action: () => scrollToSection(whyChooseRef) },
          { name: "Gift Cards", action: () => scrollToSection(whyChooseRef) }
        ]
      },
      { 
        name: "About", 
        description: "Learn more about us",
        icon: "ℹ️",
        action: () => scrollToSection(whyChooseRef),
        subItems: [
          { name: "Why Choose Us", action: () => scrollToSection(whyChooseRef) },
          { name: "Our Story", action: () => scrollToSection(whyChooseRef) },
          { name: "Join Us", action: () => scrollToSection(ctaRef) },
          { name: "Contact", action: () => scrollToSection(ctaRef) }
        ]
      }
    ]
  }
}); 