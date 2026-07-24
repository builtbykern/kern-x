import CMSSpotlightGallery from "../components/CMSSpotlightGallery"
import PathTypeKinetic from "../components/PathTypeKinetic"
import ScrollStoryStage from "../components/ScrollStoryStage"

export function App() {
  return (
    <>
      <nav className="nav">
        <a href="#story">Scroll Story Stage</a>
        <a href="#path">PathType Kinetic</a>
        <a href="#gallery">CMS Spotlight Gallery</a>
      </nav>

      <header className="hero">
        <p
          style={{
            margin: "0 0 10px",
            fontSize: 12,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "#0f6b5c",
          }}
        >
          kern-x · Framer Marketplace
        </p>
        <h1 className="brand">kern-x</h1>
        <p className="lede">
          Three production-ready Framer code components aimed at Featured and
          high views: cinematic scroll, kinetic type, and CMS-native gallery.
        </p>
      </header>

      <p className="section-label" id="story">
        01 · Interactions · $19
      </p>
      <h2 className="section-title">Scroll Story Stage</h2>
      <div className="spacer">Scroll to enter the stage</div>
      <ScrollStoryStage
        mode="Zoom"
        sectionHeightVh={280}
        accentColor="#e8ff6a"
      />

      <p className="section-label" id="path">
        02 · Typography · $12
      </p>
      <h2 className="section-title">PathType Kinetic</h2>
      <div className="path-wrap">
        <PathTypeKinetic
          mode="Path"
          pathPreset="Wave"
          text="Design that moves with you"
          color="#12201c"
          fontSize={48}
          autoPlay
        />
      </div>
      <div className="pad" style={{ maxWidth: 900, margin: "0 auto", padding: 32 }}>
        <PathTypeKinetic
          mode="ColorReveal"
          text="Scroll to reveal every word with color."
          granularity="Word"
          colorStart="rgba(18,32,28,0.2)"
          colorEnd="#12201c"
          fontSize={36}
        />
      </div>

      <p className="section-label" id="gallery">
        03 · Carousels · Free / $9
      </p>
      <h2 className="section-title">CMS Spotlight Gallery</h2>
      <CMSSpotlightGallery />

      <footer
        style={{
          padding: "48px 24px 64px",
          textAlign: "center",
          color: "rgba(18,32,28,0.55)",
          fontSize: 14,
        }}
      >
        Copy the files in <code>/components</code> into a Framer project Code
        folder to publish.
      </footer>
    </>
  )
}
