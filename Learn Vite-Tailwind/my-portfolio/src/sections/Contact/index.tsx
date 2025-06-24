import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLinkedin, faGithub, faFacebook } from '@fortawesome/free-brands-svg-icons'
import { faEnvelope } from '@fortawesome/free-regular-svg-icons'

const Contact: React.FC = () => {
    return (        
        <div className='flex items-end gap-4 text-2xl'>
              <a href='https://www.google.com' target='_blank'>
                <FontAwesomeIcon className='hover:scale-125 transition-all duration-300 ' icon={faLinkedin} />
              </a>
              <a href='https://www.google.com' target='_blank'>
                <FontAwesomeIcon className='hover:scale-125 transition-all duration-300' icon={faGithub} />
              </a>
              <a href='https://www.google.com' target='_blank'>
                <FontAwesomeIcon className='hover:scale-125 transition-all duration-300' icon={faFacebook} />
              </a>
              <a href='mailto:example@email.com'>
                <FontAwesomeIcon className='hover:scale-125 transition-all duration-300' icon={faEnvelope} />
              </a>

              
        </div> 
    )
}

export default Contact;