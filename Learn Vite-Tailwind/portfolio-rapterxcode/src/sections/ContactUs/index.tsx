import { data } from "../../contents/contact";
const ContactUs: React.FC = () => {
    return (
        <div className="mb-2">
            <div className="grid gap-y-5 px-5">
                <div className="text-mainText text-2xl font-medium">Contact Us</div>
                <div className="text-mainText ">
                    {data.map((item, index) => (
                        <div key={`contact-${index}`} className="mb-4">
                            <h3 className="font-bold">{item.title}</h3>
                            {item.link && (
                                <a href={item.link} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:text-blue-700">
                                    {item.link}
                                </a>
                            )}
                            {item.description && (
                                <div className="mt-1">
                                    {item.description.map((desc, i) => (
                                        <p key={`desc-${i}`}>{desc}</p>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default ContactUs;
