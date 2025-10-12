import '../Components/CourseInfoGrid.css';

const GridCourseInfo = (GridInfo) =>{
    return (
        <div id="gridContainer">
            <h2>{GridInfo.header}</h2>
            <h1>{GridInfo.data}</h1>
        </div>
    );
}

export default GridCourseInfo;