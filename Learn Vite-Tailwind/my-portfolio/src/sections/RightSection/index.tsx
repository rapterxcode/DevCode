import About from "../About";   
import ContentContainer from "../../components/ContentContainer";
import { data as experienceData } from "../../contents/experience";
import { data as projectData } from "../../contents/project";
import { data as contactData } from "../../contents/project";
import Footer from "../Footer";

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
                title="Contacts"
                data={contactData}
            />
            <Footer />
        </div>
    )
}

export default RightSection;