export interface HeroSlide {
  id: number;
  title: string;
  subtitle: string;
  cta: string;
  bg: string;
  icon: string;
}

export const heroSlides: HeroSlide[] = [
  { 
    id: 1,
    title: "Discover Your Next Great Read", 
    subtitle: "Explore thousands of books from bestselling authors and hidden gems", 
    cta: "Browse Collection", 
    bg: "bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700",
    icon: "🌟"
  },
  { 
    id: 2,
    title: "New Releases & Bestsellers", 
    subtitle: "Stay updated with the latest books and trending titles", 
    cta: "See What's New", 
    bg: "bg-gradient-to-br from-purple-600 via-pink-600 to-rose-700",
    icon: "✨"
  },
  { 
    id: 3,
    title: "Free Shipping on Orders Over $35", 
    subtitle: "Build your personal library with our extensive collection", 
    cta: "Start Shopping", 
    bg: "bg-gradient-to-br from-green-600 via-emerald-600 to-teal-700",
    icon: "🚚"
  },
]; 