import About from "../About";   
import ContentContainer from "../../components/ContentContainer";
import { data as experienceData } from "../../contents/experience";
import { data as projectData } from "../../contents/project";
import { data as certificationData } from "../../contents/certification";
import { data as educationData } from "../../contents/education";
import Footer from "../Footer";
import ContactUs from "../ContactUs";
interface RightSectionProps {
    onInit?: (sectionId: string) => void;
}

const RightSection: React.FC<RightSectionProps> = ({ onInit }) => {
    return (
        <div className="grid gap-y-5 px-5">
            <About
                title="About"
                onInit={onInit}
            />
            <ContentContainer 
                onInit={onInit}
                title="Education"
                data={educationData}
            />
            <ContentContainer
                onInit={onInit}
                title="Experiences"
                data={experienceData}
            />
            <ContentContainer
                onInit={onInit}
                title="Projects"
                data={projectData}
            />
            <ContentContainer
                onInit={onInit}
                title="Certification"
                data={certificationData}
            />
            <ContactUs />
            <Footer />
        </div>
    )
}

export default RightSection;