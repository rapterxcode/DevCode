import Contact from "../Contact";
import Navbar from "../Navbar";
import Header from "../Header";

interface NavItem {
  title: string;
  sectionId: string;
}

interface LeftSectionProps {
  navBarItems: NavItem[];
  currentSection: string;
}

const LeftSection: React.FC<LeftSectionProps> = ({ navBarItems, currentSection }) => {
    return (
        <div className="px-5">
            <div className='sticky top-14 px-5 grid gap-y-2 lg:grid-rows-[1fr_2fr_20%] lg:h-[95vh]'>
            <Header />
            <Navbar navBarItems={navBarItems} currentSection={currentSection} />
            <Contact />
            </div>
        </div>
    )
}

export default LeftSection;