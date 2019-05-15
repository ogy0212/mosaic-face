import React from 'react';
import logo from './logo.svg';
import './App.css';

const createObjectURL = (window.URL || window.webkitURL).createObjectURL || window.createObjectURL;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      image_src: '',
      file: null,
      mosaic_image_src: '',
      mosaic_file: null,
    }
  }

  handleChangeFile(e) {
    const files = e.target.files;
    const image_url = files.length === 0 ? '' : createObjectURL(files[0]);
    this.setState({
      image_src: image_url,
      file: files[0]
    });
  }

  sendImage() {
    const formData = new FormData();
    formData.append('myFile', this.state.file);
    fetch('/api/upload', { method: 'POST', body: formData }).then(response => {
      return response.blob();
    }).then(imageBlob => {
      console.log(imageBlob);
      const response_file_url = createObjectURL(imageBlob);
      this.setState({
        mosaic_image_src: response_file_url,
        mosaic_file: imageBlob,
      })
    })
  }

  render() {
    return (
      <div>
        <div>
          <input type="file" ref="file" onChange={this.handleChangeFile.bind(this)} />
        </div>
        <div>
          <img id="original-image" src={this.state.image_src} alt="nothing." />
        </div>
        <div>
          <button onClick={this.sendImage.bind(this)}>変換する</button>
        </div>
        <div>
        <img id="mosaic-image" src={this.state.mosaic_image_src} alt="nothing." />
        </div>
      </div>
    );
  }
}

export default App;
