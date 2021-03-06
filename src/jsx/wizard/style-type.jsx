var StyleType = React.createClass({
  statics: {
    navigationTitle: 'Style'
  },
  render: function() {
    return(
      <main>

        {
          this.props.mediaType !== 'web3d' ?

          <div className="option">
            <h1>
              Realistic
            </h1>

            <div className="description">
              A realistically-oriented style.
            </div>

            <div>
              <button className="btn btn-primary" onClick={this.props.navigate.bind(null, ModifierType, { styleType: 'realistic' })}>
                Choose
              </button>
            </div>
          </div>

          :

          null
        }

        {
          this.props.mediaType !== 'web3d' ?

          <div className="option">
            <h1>
              Illustrated
            </h1>

            <div className="description">
              A blueprint-like, line-based aesthetic.
            </div>

            <div>
              <button className="btn btn-primary" onClick={this.props.navigate.bind(null, ModifierType, { styleType: 'illustrated' })}>
                Choose
              </button>
            </div>
          </div>

          :

          null
        }

        {
          this.props.mediaType === 'web3d' ?

          <div className="option">
            <h1>
              Realtime
            </h1>

            <div className="description">
              The default realtime style.
            </div>

            <div>
              <button className="btn btn-primary" onClick={this.props.navigate.bind(null, ModifierType, { styleType: 'realtime' })}>
                Choose
              </button>
            </div>
          </div>

          :

          null
        }

      </main>
    );
  }
});
