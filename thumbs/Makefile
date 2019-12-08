requirements.txt: Pipfile.lock
	pipenv run pip freeze > requirements.txt
	touch -r Pipfile.lock requirements.txt

.package: requirements.txt
	rm -rf .package
	pip install --requirement requirements.txt --target .package
	touch -r requirements.txt .package

EXCLUDE_PATTERNS=\*/__pycache__/\* botocore/data/ec2/\* botocore/data/cloudfront/\* botocore/data/rds/\* django/contrib/\* PIL/.libs/libfreetype\* thumbs/\*

package.zip: src/* .package
	rm -f package.zip
	for d in src .package; do \
		echo $$d ; \
		cd $$d ; \
		zip -x ${EXCLUDE_PATTERNS} @ -r9 ../package.zip . ; \
		cd - ; \
	done

.PHONY: deploy_s3
deploy_s3: package.zip
	aws lambda update-function-code --function-name arn:aws:lambda:eu-west-1:929325949831:function:el-resize-image --zip-file fileb://package.zip --publish
	@echo '⏳ Update the Lambda function ARN on https://s3.console.aws.amazon.com/s3/buckets/data.electionleaflets.org/?region=eu-west-1&tab=properties -> Events'
	@echo 'with the FunctionArn returned above.'

.PHONY: deploy_s3
deploy_cf: package.zip
	aws lambda update-function-code --region=us-east-1 --function-name arn:aws:lambda:us-east-1:929325949831:function:el-thumbnail --zip-file fileb://package.zip --publish
	@echo '⏳ Update the "thumbs/*" behaviour on https://console.aws.amazon.com/cloudfront/home?region=us-east-1#distribution-settings:E2FHP2ULXIVMLT'
	@echo 'with the FunctionArn returned above.'
