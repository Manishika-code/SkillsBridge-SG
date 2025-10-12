import '../Components/CourseRoadMapList.css';

const CourseRoadMapList = (roadMap) =>{
    return (
        <div className='roadMapItem'>
            <h4>{roadMap.itemName}</h4>
        </div>
    );
}
export default CourseRoadMapList;