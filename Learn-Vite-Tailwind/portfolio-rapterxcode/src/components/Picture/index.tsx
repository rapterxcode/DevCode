interface PictureProps {
    picture: string;
    title: string;
}

const Picture: React.FC<PictureProps> = ({picture, title}) => {
    if (!picture) return null;
    return (
        <div>
            <img src={picture} alt={title} className="w-5/6 rounded-md border-2 mt-6 border-mainContainerBg" />
        </div>
    )
}

export default Picture;