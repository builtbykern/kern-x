import LogoMarquee from "../code/LogoMarquee"
import PageProgress from "../code/PageProgress"
import StatCountUp from "../code/StatCountUp"

export function App() {
  return (
    <>
      <PageProgress position="Top" color="#0f6b5c" height={3} />

      <nav className="nav">
        <a href="#countup">Stat CountUp</a>
        <a href="#marquee">Logo Marquee</a>
        <a href="#progress">Page Progress</a>
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
          kern-x · Framer handoff
        </p>
        <h1 className="brand">kern-x</h1>
        <p className="lede">
          Three simple, useful Framer code components: metrics, trusted-by
          logos, and reading progress. Copy from <code>/code</code> into
          another Framer project.
        </p>
      </header>

      <p className="section-label" id="countup">
        01 · Data · Free / $5
      </p>
      <h2 className="section-title">Stat CountUp</h2>
      <div
        style={{
          maxWidth: 900,
          margin: "0 auto",
          padding: "24px 24px 64px",
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
          gap: 32,
        }}
      >
        <div>
          <StatCountUp to={12000} suffix="+" color="#12201c" />
          <p style={{ margin: "8px 0 0", color: "rgba(18,32,28,0.55)" }}>
            Active users
          </p>
        </div>
        <div>
          <StatCountUp
            to={98}
            suffix="%"
            useCommas={false}
            color="#12201c"
          />
          <p style={{ margin: "8px 0 0", color: "rgba(18,32,28,0.55)" }}>
            Retention
          </p>
        </div>
        <div>
          <StatCountUp
            from={0}
            to={2.4}
            decimals={1}
            prefix="$"
            suffix="M"
            useCommas={false}
            color="#12201c"
          />
          <p style={{ margin: "8px 0 0", color: "rgba(18,32,28,0.55)" }}>
            Arr booked
          </p>
        </div>
      </div>

      <p className="section-label" id="marquee">
        02 · Carousels · Free / $5–9
      </p>
      <h2 className="section-title">Logo Marquee</h2>
      <div style={{ padding: "16px 0 64px", background: "#fff" }}>
        <LogoMarquee background="#ffffff" logoHeight={36} gap={56} speed={36} />
      </div>

      <p className="section-label" id="progress">
        03 · Interactions · Free
      </p>
      <h2 className="section-title">Page Progress</h2>
      <div className="spacer" style={{ height: "70vh" }}>
        Scroll the page — the top bar tracks reading progress
      </div>
      <div className="spacer" style={{ height: "50vh" }}>
        Keep going…
      </div>

      <footer
        style={{
          padding: "48px 24px 64px",
          textAlign: "center",
          color: "rgba(18,32,28,0.55)",
          fontSize: 14,
        }}
      >
        Handoff: copy each file from <code>/code</code> into Framer Assets →
        Code.
      </footer>
    </>
  )
}
