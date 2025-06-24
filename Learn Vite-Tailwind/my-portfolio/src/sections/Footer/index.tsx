import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCopyright } from "@fortawesome/free-solid-svg-icons";
const Footer: React.FC = () => {
    return (
        <div className="mb-2">
            <div className="flex justify-end text-mainText">
                <span><FontAwesomeIcon icon={faCopyright} /> 2025 All rights reserved </span>
            </div>
        </div>
    )
}

export default Footer;


