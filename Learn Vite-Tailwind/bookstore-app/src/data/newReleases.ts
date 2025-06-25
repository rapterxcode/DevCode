import type { Book } from './featuredBooks';

export const newReleases: Book[] = [
  { 
    id: 1, 
    title: "Fourth Wing", 
    author: "Rebecca Ross", 
    genre: "Fantasy", 
    price: 26.99, 
    image: [
      "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=600&fit=crop", 
      "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=600&fit=crop&flip=h"
    ], 
    isNew: true, 
    color: "from-purple-600 to-indigo-600",
    rating: 4.8,
    description: "A thrilling fantasy novel about dragons and destiny."
  },
  { 
    id: 2, 
    title: "Tomorrow, and Tomorrow", 
    author: "Gabrielle Zevin", 
    genre: "Literary Fiction", 
    price: 28.99, 
    image: [
      "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=600&fit=crop"
    ], 
    isNew: true, 
    color: "from-blue-600 to-purple-600",
    rating: 4.6,
    description: "A literary masterpiece exploring love and loss."
  },
  { 
    id: 3, 
    title: "The Atlas Six", 
    author: "Olivie Blake", 
    genre: "Dark Academia", 
    price: 24.99, 
    image: [
      "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop", 
      "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop&flip=v"
    ], 
    isNew: true, 
    color: "from-indigo-600 to-purple-600",
    rating: 4.7,
    description: "A dark academic thriller with magical elements."
  },
  { 
    id: 4, 
    title: "Project Hail Mary", 
    author: "Andy Weir", 
    genre: "Sci-Fi", 
    price: 23.99, 
    image: [
      "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&h=600&fit=crop"
    ], 
    isNew: true, 
    color: "from-cyan-600 to-blue-600",
    rating: 4.9,
    description: "An epic space adventure from the author of The Martian."
  },
]; 