import React, {useState} from 'react';
import '../Components/Dropdown.css';
import { FaChevronDown } from "react-icons/fa";
import { FaChevronUp } from "react-icons/fa";

function Dropdown({ options, placeholder = 'Select option', onDropdownSelect}) {
    
    const [isOpen, setIsOpen] = useState(false);
    const [selectedOption, setSelectedOption] = useState('');

    const handleDropdownClick = (option) => {
        setSelectedOption(option.label);
        setIsOpen(false);

        if (onDropdownSelect){
            onDropdownSelect(option);
        }
    }

    return (
        <div className='dropdown' onMouseEnter ={() => setIsOpen(true)} onMouseLeave={() => setIsOpen(false)}>
            <div className='dropdown_header'>
                {selectedOption || placeholder}
                <span className='arrow'>{isOpen ? <FaChevronUp /> : <FaChevronDown />}</span>
            </div>

            {isOpen && (
                <div className='dropdown_panel'>
                    {options.map((opt) => (
                        <div 
                        key={opt.value}
                        className='dDitem'
                        onClick={() => handleDropdownClick(opt)}
                        >
                            {opt.label}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
export default Dropdown;