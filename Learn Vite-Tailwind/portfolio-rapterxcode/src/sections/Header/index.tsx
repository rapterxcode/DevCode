import { faArrowDown } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { data } from "../../contents/header";

const Header: React.FC = () => {
    return (
        <div className='flex flex-col gap-2'>
            <div className='flex justify-center mx-auto mb-10'><img className="object-cover object-center rounded-full w-56 h-56 border-2 border-mainContainerBg " src={data.thumbnail} alt="image description"/></div>
              <div className='font-bold text-mainText text-4xl'>{data.title}</div>
              <div className='font-semibold text-mainText'>{data.position}</div>
              
              <div className='text-sm text-mainText w-5/6'>{data.description2}</div>
              <div className='mt-4'>
                <a href={data.resumeFile} target='_blank'>
                  <span className='rounded-md bg-mainButtonBg py-2 px-4 font-bold text-mainButtonText'>
                    {data.resume}
                    <span className='rotate-90 inline-block ml-2 text-sm'><FontAwesomeIcon className='animate-bounce' icon={faArrowDown} /></span>
                  </span>
                </a>
              </div>
        </div>
    )
}

export default Header;