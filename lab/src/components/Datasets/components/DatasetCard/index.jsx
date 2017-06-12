import React, { Component } from 'react';
import { connect } from 'react-redux';
import * as actions from './data/actions';
import DatasetActions from './components/DatasetActions';

import { BestResultSegment } from './components/BestResultSegment';
import { ExperimentsSegment } from './components/ExperimentsSegment';
import { Grid, Segment, Header, Button } from 'semantic-ui-react';

// BestResults
// ExperimentStatus
// BuilderButton

class DatasetCard extends Component {
	getDatasetLink() {
		const id = this.props.dataset.get('_id');
		return `/#/datasets/${id}`;
	}

	getBuilderLink() {
		const id = this.props.dataset.get('_id');
		return `/#/build/${id}`;
	}

	// make this into own component
	renderBestResult() {
		const hasMetadata = this.props.dataset.get('has_metadata');
		const bestResult = this.props.dataset.get('best_result');

		if(!hasMetadata) {
			return (
				<Segment inverted attached className="panel-body">
					You must upload a metadata file in order to use this dataset. 
					Please follow the instructions here.
				</Segment>
			);
		}

		if(!bestResult) {
			return (
				<Segment inverted attached className="panel-body">
					No results yet, build a new experiment to start.
				</Segment>
			);
		}
		
		return <BestResultSegment result={bestResult} />;
	}

	render() {
		const { dataset } = this.props;
		return (
			<Grid.Column className="dataset-card">
				<Segment inverted attached="top" className="panel-header">
					<Header 
						as="a"
						inverted 
						size="large"
						content={dataset.get('name')}
						href={this.getDatasetLink()}
						className="title"
					/>
					<span className="float-right">
						<DatasetActions {...this.props} />
					</span>
				</Segment>
				{this.renderBestResult()}
				<ExperimentsSegment
					datasetName={dataset.get('name')}
					experiments={dataset.get('experiments')}
					notifications={dataset.get('notifications')}
				/>
				<Button
					as="a"
					color="blue"
					attached="bottom"
					content="Build New Experiment"
					href={this.getBuilderLink()}
				/>
			</Grid.Column>
		);
	}
}

DatasetCard = connect(
	null,
	actions
)(DatasetCard);

export default DatasetCard;