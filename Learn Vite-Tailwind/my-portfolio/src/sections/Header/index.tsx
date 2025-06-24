import { faArrowDown } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { data } from "../../contents/header";
const Header: React.FC = () => {
    return (
        <div className='flex flex-col gap-2'>
              <div className='font-bold text-primaryTitle text-4xl'>{data.title}</div>
              <div className='font-semibold text-primaryContent'>{data.position}</div>
              <div className='text-sm w-5/6'>{data.description2}</div>
              <div className='mt-4'>
                <a href={data.resumeFile} target='_blank'>
                  <span className='rounded-md bg-primaryTitle py-2 px-4 text-white'>
                    {data.resume}
                    <span className='rotate-90 inline-block ml-2 text-sm'><FontAwesomeIcon className='animate-bounce' icon={faArrowDown} /></span>
                  </span>
                </a>
              </div>
        </div>
    )
}

export default Header;