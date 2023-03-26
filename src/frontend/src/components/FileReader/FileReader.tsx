import React, {ChangeEvent, useState} from 'react';
import Papa from 'papaparse';
import './FileReader.css';

const FileReader = () => {
  const [file, setFile] = useState<File>();

  const handleChange = (event: ChangeEvent): void => {
    const target = event.target as HTMLInputElement;
    if (!target || !target.files) {
      return;
    }
    const newFile = target.files[0];
    setFile(newFile);
    Papa.parse(newFile, {
      header: true,
      download: true,
      skipEmptyLines: true,
      complete: () => { console.log(newFile) },
    });
  };

  const postData = (file: File): void => {
    fetch('/predict/demand', {
      method: 'POST',
      body: file,
      headers: {
        'content-types': file.type,
        'content-length': `${file.size}`,
      }
    })
      .then((res) => res.json())
      .then((data) => console.log(data))
      .catch((err) => console.error(err));
  };

  return (
    <div className='file-reader'>
      <div className='file-reader__title title col'>
        Введите данные:
      </div>
      <div className='file-reader__input col'>
        <button className='file-reader__button'>
          <label htmlFor='csv-input'>Прикрепить файл</label>
          <input
            className='csv-input'
            type='file'
            onChange={handleChange}
            id='csv-input'
          />
        </button>
      </div>
    </div>
  )
};

export default FileReader;
