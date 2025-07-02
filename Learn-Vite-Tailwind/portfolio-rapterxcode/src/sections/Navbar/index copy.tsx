import { faArrowRight } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"

/* const navs = [
  {
    title:"About", sectionnId:"About-section"
  },
  {
    title:"Experiences", sectionnId:"Experience-section"
  },
  {
    title:"Projects", sectionnId:"Projects-section"
  }
] */


const Navbar: React.FC = () => {


    return (
        <div className='flex flex-col gap-3 font-semibold text-primaryContent'>
             
              <div>
                <FontAwesomeIcon className='mr-2 text-primaryTitle' icon={faArrowRight} />
                About</div>
              <div>Experience</div>
              <div>Projects</div>
              <div>Contact</div>
        </div>
    )   
}

export default Navbar;