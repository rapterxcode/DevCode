export interface WhyChooseFeature {
  id: number;
  icon: string;
  title: string;
  description: string;
}

export interface WhyChooseData {
  title: string;
  subtitle: string;
  features: WhyChooseFeature[];
}

export const whyChooseData: WhyChooseData = {
  title: "Why BookHaven?",
  subtitle: "More than just a bookstore - we're your reading companion",
  features: [
    {
      id: 1,
      icon: "🚚",
      title: "Free Shipping",
      description: "Free delivery on orders over $35. Fast, secure, and reliable shipping worldwide."
    },
    {
      id: 2,
      icon: "💯",
      title: "Satisfaction Guarantee",
      description: "30-day return policy. Not happy with your purchase? Return it hassle-free."
    },
    {
      id: 3,
      icon: "🎯",
      title: "Personalized Recommendations",
      description: "AI-powered suggestions based on your reading history and preferences."
    }
  ]
}; 