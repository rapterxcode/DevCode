export interface Book {
  id: number;
  title: string;
  author: string;
  genre: string;
  price: number;
  originalPrice?: number;
  image: string[];
  rating: number;
  description: string;
  color: string;
  isNew?: boolean;
}

export const featuredBooks: Book[] = [
  { 
    id: 1, 
    title: "The Seven Husbands of Evelyn Hugo", 
    author: "Taylor Jenkins Reid", 
    genre: "Fiction",
    price: 24.99, 
    originalPrice: 32.99, 
    image: [
      "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=600&fit=crop", 
      "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=600&fit=crop&flip=h",
      "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=600&fit=crop&flip=v"
    ], 
    rating: 4.8,
    description: "A captivating novel about a reclusive Hollywood icon who finally decides to tell her story to a young journalist.",
    color: "from-purple-500 to-pink-500"
  },
  { 
    id: 2, 
    title: "Atomic Habits", 
    author: "James Clear", 
    genre: "Self-Help",
    price: 18.99, 
    originalPrice: 24.99, 
    image: [
      "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400&h=600&fit=crop&flip=h"
    ], 
    rating: 4.9,
    description: "An easy & proven way to build good habits & break bad ones. Transform your life with tiny changes.",
    color: "from-blue-500 to-cyan-500"
  },
  { 
    id: 3, 
    title: "Where the Crawdads Sing", 
    author: "Delia Owens", 
    genre: "Mystery",
    price: 22.99, 
    originalPrice: 28.99, 
    image: [
      "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=400&h=600&fit=crop", 
      "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=400&h=600&fit=crop&flip=v",
      "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=400&h=600&fit=crop&flip=h"
    ], 
    rating: 4.7,
    description: "A beautiful coming-of-age story and murder mystery set in the marshlands of North Carolina.",
    color: "from-green-500 to-emerald-500"
  },
  { 
    id: 4, 
    title: "The Silent Patient", 
    author: "Alex Michaelides", 
    genre: "Thriller",
    price: 19.99, 
    originalPrice: 26.99, 
    image: [
      "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=600&fit=crop&flip=h"
    ], 
    rating: 4.6,
    description: "A psychological thriller about a woman who refuses to speak after allegedly murdering her husband.",
    color: "from-red-500 to-orange-500"
  },
  { 
    id: 5, 
    title: "The Midnight Library", 
    author: "Matt Haig", 
    genre: "Fiction",
    price: 21.99, 
    originalPrice: 29.99, 
    image: [
      "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop", 
      "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop&flip=h",
      "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop&flip=v"
    ], 
    rating: 4.5,
    description: "Between life and death there is a library, and within that library, the shelves go on forever. Every book provides a chance to try another life you could have lived.",
    color: "from-indigo-500 to-purple-500"
  },
  { 
    id: 6, 
    title: "Educated", 
    author: "Tara Westover", 
    genre: "Memoir",
    price: 20.99, 
    originalPrice: 27.99, 
    image: [
      "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=600&fit=crop&flip=h"
    ], 
    rating: 4.7,
    description: "A memoir of family, resilience and self-invention. An unforgettable story about the transformative power of education.",
    color: "from-teal-500 to-cyan-500"
  },
]; 