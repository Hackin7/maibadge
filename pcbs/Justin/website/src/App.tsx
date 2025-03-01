import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";

const App: React.FC = () => {
  return (
    <div className="full-width">
      {/* Header */}
      <header className="container-fluid bg-dark text-white text-center pt-5 pb-2">
        <h1>Maibadge PCB Project</h1>
        <p>
          Custom PCBs for the arcade game Maimai, designed for makers and
          enthusiasts.
        </p>
      </header>

      <section className="container-fluid px-0 mt-8">
        <div className="row mx-4">
          {/* Flashlight section */}
          <div className="col-md-6 text-center">
            <h3>Flashlight PCB</h3>
            <p>Custom Flashlight PCB with Maimai designs.</p>
            <div className="ratio ratio-1x1">
              <iframe
                src="https://www.youtube.com/embed/uLmpFSaINYI"
                title="Flashlight"
                className="mt-1 mx-0"
              ></iframe>
            </div>
          </div>
          {/* Maibadge section */}
          <div className="col-md-6 text-center">
            <h3>Maibadge PCB</h3>
            <p>Maimai Badge PCB for personalization and style.</p>
            <div className="ratio ratio-1x1">
              <iframe
                src="https://youtube.com/embed/bU8o2R4BDwI"
                title="Maibadge"
                className="mt-1"
              ></iframe>
            </div>
          </div>
        </div>
      </section>

      {/* Contacts section */}
      <footer className="container-fluid bg-light py-8 text-center">
        <h2>Contact Us</h2>
        <h4>Send us a message for inquiries or orders.</h4>
        <p>Email: zunmun@gmail.com</p>
      </footer>
    </div>
  );
};

export default App;
